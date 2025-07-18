# Standard library imports
import os
from datetime import datetime, date, timezone

# Third-party imports
import openai
from dotenv import load_dotenv
from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy import func
from sqlalchemy.orm import joinedload

# Local application imports
from models import Producto, Categoria, Subcategoria, Articulo, ContactMessage, Testimonial, Advertisement, Afiliado, EstadisticaAfiliado, AdsenseConfig
from forms import PublicTestimonialForm
from extensions import db # Corrected 'De extensiones Importar DB'

# Load environment variables as early as possible
load_dotenv()

# Define the 'publico' Blueprint
bp = Blueprint('publico', __name__)

# Debug line to check API key loading
print(f"DEBUG (public.py): OPENAI_API_KEY value loaded: {os.getenv('OPENAI_API_KEY')}")

# Configure the OpenAI client
try: # Corrected 'Intente:'
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e: # Corrected 'excepto la excepción como e:'
    print(f"Error initializing OpenAI client in public.py: {e}. Ensure OPENAI_API_KEY is configured.")
    openai_client = None

# --- Helper functions for chatbot tools ---

def get_all_products_for_chatbot():
    """
    Retrieves all products from the database and formats them for the chatbot.
    Returns a list of dictionaries containing product ID, name, price, description, and link.
    Handles possible database errors.
    """
    try: # Corrected 'Intente:'
        products = Producto.query.all()
        products_data = []
        for p in products:
            products_data.append({
                "id": p.id,
                "name": p.nombre,
                "price": p.precio,
                "description": p.descripcion,
                "link": p.link
            })
        return products_data
    except Exception as e: # Corrected 'excepto la excepción como e:'
        print(f"Error getting products for chatbot: {e}")
        return []

def get_product_by_name_for_chatbot(product_name):
    """
    Retrieves details of a specific product by its name, formatted for the chatbot.
    Performs a case-insensitive search.
    Returns a dictionary with product details or a message if not found or an error occurs.
    """
    try:
        product = Producto.query.filter(func.lower(Producto.nombre) == func.lower(product_name)).first()
        if product:
            return {
                "id": product.id,
                "name": product.nombre,
                "price": product.precio,
                "description": product.descripcion,
                "link": product.link
            }
        return {"message": f"Product '{product_name}' not found."}
    except Exception as e:
        print(f"Error getting product by name for chatbot: {e}")
        return {"error": f"Could not retrieve product by name: {str(e)}"}

def get_available_categories():
    """
    Retrieves all product categories and returns their names as a list.
    Handles possible database errors.
    """
    try:
        categories = [cat.nombre for cat in Categoria.query.all()]
        return {"categories": categories}
    except Exception as e:
        print(f"Error getting available categories: {e}")
        return {"error": f"Could not retrieve categories: {str(e)}"}

def get_shipping_info():
    """
    Provides general information about the store's shipping policies.
    """
    return {"shipping_info": "We offer nationwide shipping. Estimated delivery time is 3 to 5 business days. For specific tracking, please visit our contact section."}

def get_contact_info():
    """
    Provides contact information for customer support, including a dynamic URL to the contact page.
    """
    contact_url = url_for('publico.contacto', _external=True)
    return {"contact_info": f"You can contact our support team by visiting our contact section at {contact_url} or by sending an email to soporte@afiliadosonline.com."}

def get_general_help_info():
    """
    Provides general information on where to find help and guides, including a dynamic URL to the guides section.
    """
    guides_url = url_for('publico.guias', _external=True)
    return {"help_info": f"You can find detailed guides and additional help in our Guides section: {guides_url}."}

### Context Processors


@bp.context_processor
def inject_active_advertisements():
    """
    Injects a list of active advertisements into the template context.
    Advertisements are filtered by is_active=True and by start/end dates if defined.
    """
    now_utc = datetime.now(timezone.utc)
    active_ads = Advertisement.query.options(joinedload(Advertisement.product)).filter(
        Advertisement.is_active,
        (Advertisement.start_date.is_(None)) | (Advertisement.start_date <= now_utc),
        (Advertisement.end_date.is_(None)) | (Advertisement.end_date >= now_utc)
    ).all()
    return dict(active_advertisements=active_ads)

@bp.context_processor
def inject_adsense_config():
    """
    Injects the global AdSense configuration into the template context,
    fetching the data from the database.
    """
    adsense_config_db = AdsenseConfig.query.first()
# In routes/public.py, inside inject_adsense_config

    if adsense_config_db: # Corrected 'Si' to 'if'
        return dict(
            adsense_client_id=adsense_config_db.adsense_client_id, # Added this back
            adsense_slot_header=adsense_config_db.adsense_slot_1, # Assuming slot_1 for header
            adsense_slot_sidebar=adsense_config_db.adsense_slot_2, # Corrected to use existing slot_2
            adsense_slot_content=adsense_config_db.adsense_slot_3, # Corrected to use existing slot_3
            adsense_slot_footer='' # Or assign another existing slot, or keep it empty if not available
        )
    else: # Corrected 'más' to 'else'
        return dict(
            adsense_client_id='',
            adsense_slot_header='',
            adsense_slot_sidebar='',
            adsense_slot_content='',
            adsense_slot_footer=''
        )


@bp.route('/')
def index():
    """Renders the main index page with paginated products."""
    page = request.args.get('page', 1, type=int)
    per_page = 9
    productos_pagination = Producto.query.order_by(Producto.fecha_creacion.desc()).paginate(page=page, per_page=per_page, error_out=False)
    productos = productos_pagination.items
    total_pages = productos_pagination.pages
    return render_template('index.html', productos=productos, page=page, total_pages=total_pages)

@bp.route('/producto/<slug>')
def product_detail(slug):
    """Renders the detail page for a specific product based on its slug."""
    producto = Producto.query.filter_by(slug=slug).first()
    if producto:
        return render_template('product_detail.html', product=producto)
    flash('Producto no encontrado.', 'danger')
    return redirect(url_for('publico.index'))

@bp.route('/categorias')
def show_categorias():
    """Renders the categories page, displaying all categories and product counts per subcategory."""
    categorias = Categoria.query.all()
    product_counts_raw = db.session.query(
        Subcategoria.id,
        func.count(Producto.id)
    ).outerjoin(Producto, Subcategoria.id == Producto.subcategoria_id) \
        .group_by(Subcategoria.id) \
        .all()
    product_counts_dict = {sub_id: count for sub_id, count in product_counts_raw}
    return render_template(
        'categorias.html',
        categorias=categorias,
        product_counts=product_counts_dict
    )

@bp.route('/productos/<slug>')
def productos_por_slug(slug):
    """Renders a page displaying products within a specific subcategory based on its slug."""
    subcat = Subcategoria.query.filter_by(slug=slug).first()
    if subcat:
        page = request.args.get('page', 1, type=int)
        per_page = 9
        products_pagination = Producto.query.filter_by(subcategoria_id=subcat.id).paginate(page=page, per_page=per_page, error_out=False)
        products_in_subcat = products_pagination.items
        total_pages = products_pagination.pages
        return render_template('productos_por_subcategoria.html',
                               subcat_name=subcat.nombre,
                               productos=products_in_subcat,
                               page=page, # Corrected 'página=página,'
                               total_pages=total_pages)
    flash('Subcategoría no encontrada.', 'danger')
    return redirect(url_for('publico.show_categorias'))

@bp.route('/guias')
def guias():
    """Renders the guides page with paginated articles."""
    page = request.args.get('page', 1, type=int)
    per_page = 6
    articulo_pagination = Articulo.query.order_by(Articulo.fecha.desc()).paginate(page=page, per_page=per_page, error_out=False)
    articulos_db = articulo_pagination.items
    total_pages = articulo_pagination.pages
    articulos = []
    for art in articulos_db:
        fecha_dt = art.fecha
        if isinstance(art.fecha, date) and not isinstance(art.fecha, datetime):
            fecha_dt = datetime.combine(art.fecha, datetime.min.time()).replace(tzinfo=timezone.utc)
        elif isinstance(art.fecha, datetime) and art.fecha.tzinfo is None:
            fecha_dt = art.fecha.replace(tzinfo=timezone.utc)

        articulos.append({
            "titulo": art.titulo,
            "slug": art.slug,
            "contenido": art.contenido,
            "fecha_iso": fecha_dt.strftime("%Y-%m-%d") if fecha_dt else "",
            "fecha_formateada": fecha_dt.strftime("%d %b %Y") if fecha_dt else "",
        })
    return render_template('guias.html', articulos=articulos, page=page, total_pages=total_pages)

@bp.route('/guia/<slug>')
def guia_detalle(slug):
    """Renders the detail page for a specific article based on its slug."""
    articulo = Articulo.query.filter_by(slug=slug).first()
    if articulo:
        if isinstance(articulo.fecha, date) and not isinstance(articulo.fecha, datetime):
            articulo.fecha = datetime.combine(articulo.fecha, datetime.min.time()).replace(tzinfo=timezone.utc)
        elif isinstance(articulo.fecha, datetime) and articulo.fecha.tzinfo is None:
            articulo.fecha = articulo.fecha.replace(tzinfo=timezone.utc)
        return render_template('guia_detalle.html', articulo=articulo)
    flash('Artículo no encontrado.', 'danger')
    return redirect(url_for('publico.guias'))




# ... (otras importaciones y funciones) ...

@bp.route('/acerca-de', methods=['GET', 'POST'])
def acerca_de():
    testimonial_form = PublicTestimonialForm()

    if testimonial_form.validate_on_submit():
        # Honeypot check for spam
        if testimonial_form.fax_number.data:
            print("Spam detected: honeypot field filled for testimonial submission.")
            flash('Gracias por tu testimonio. Ha sido recibido.', 'success')
            return redirect(url_for('publico.acerca_de'))

        try:
            new_testimonial = Testimonial(
                author=testimonial_form.author.data,
                content=testimonial_form.content.data,
                is_visible=False, # Testimonials are not visible by default, awaiting admin approval
                date_posted=datetime.now(timezone.utc)
            )
            db.session.add(new_testimonial)
            db.session.commit()
            flash('¡Gracias por tu testimonio! Será revisado y, si es aprobado, aparecerá pronto en nuestra página.', 'success')
            return redirect(url_for('publico.acerca_de'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al enviar tu testimonio. Por favor, inténtalo de nuevo. Detalles: {e}', 'danger')
            print(f"Error saving testimonial: {e}")

    # ¡IMPORTANTE!: Cambia 'testimonios' a 'testimonials' aquí
    testimonials = Testimonial.query.filter_by(is_visible=True).order_by(Testimonial.date_posted.desc()).all()
    return render_template('about.html', testimonials=testimonials, testimonial_form=testimonial_form)

# ... (resto de tu public.py) ...
@bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Renders the contact page and handles form submissions."""
    errors = {}
    success = False

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        fax_number = request.form.get('fax_number')

        if not nombre:
            errors['nombre'] = 'El nombre es obligatorio.'
        if not email or '@' not in email:
            errors['email'] = 'Introduce un correo electrónico válido.'
        if not mensaje:
            errors['mensaje'] = 'El mensaje es obligatorio.'

        if fax_number:
            print("Spam detected: honeypot field filled.")
            return redirect(url_for('publico.contacto'))

        if not errors:
            try:
                new_message = ContactMessage(
                    name=nombre,
                    email=email,
                    message=mensaje,
                    timestamp=datetime.now(timezone.utc)
                )
                db.session.add(new_message)
                db.session.commit()
                flash('¡Gracias! Tu mensaje ha sido enviado correctamente. Nos pondremos en contacto contigo pronto.', 'success')
                success = True
                return render_template('contact.html', success=success, errors={})
            except Exception as e:
                db.session.rollback()
                flash(f'Ocurrió un error al enviar tu mensaje: {e}', 'danger')
                print(f"Error saving contact message: {e}")
                errors['general'] = 'Ocurrió un error al enviar tu mensaje. Inténtalo de nuevo.'

    return render_template('contact.html', success=success, errors=errors)

@bp.route('/politica-de-privacidad')
def privacy_policy():
    """Renders the privacy policy page."""
    return render_template('privacy_policy.html')

@bp.route('/terminos-condiciones')
def terms_conditions():
    """Renders the terms and conditions page."""
    return render_template('terms_conditions.html')

@bp.route('/politica-de-cookies')
def cookie_policy():
    """Renders the cookie policy page."""
    return render_template('cookie_policy.html')

@bp.route('/sitemap.xml')
def sitemap():
    """Generates and serves the sitemap.xml for SEO."""
    base_url = request.url_root.rstrip('/')
    urls = [
        {"loc": base_url + url_for('publico.index'), "changefreq": "daily", "priority": "1.0"},
        {"loc": base_url + url_for('publico.show_categorias'), "changefreq": "weekly", "priority": "0.8"},
        {"loc": base_url + url_for('publico.acerca_de'), "changefreq": "monthly", "priority": "0.7"},
        {"loc": base_url + url_for('publico.contacto'), "changefreq": "monthly", "priority": "0.6"},
        {"loc": base_url + url_for('publico.guias'), "changefreq": "weekly", "priority": "0.9"},
        {"loc": base_url + url_for('publico.privacy_policy'), "changefreq": "monthly", "priority": "0.5"},
        {"loc": base_url + url_for('publico.terms_conditions'), "changefreq": "monthly", "priority": "0.5"},
        {"loc": base_url + url_for('publico.cookie_policy'), "changefreq": "monthly", "priority": "0.5"},
    ]
    for product in Producto.query.all():
        urls.append({
            "loc": f"{base_url}{url_for('publico.product_detail', slug=product.slug)}",
            "changefreq": "weekly",
            "priority": "0.8"
        })
    for articulo in Articulo.query.all():
        urls.append({
            "loc": f"{base_url}{url_for('publico.guia_detalle', slug=articulo.slug)}",
            "changefreq": "weekly",
            "priority": "0.8"
        })
    return render_template('sitemap.xml', urls=urls, today=datetime.now().strftime("%Y-%m-%d"))

@bp.route('/robots.txt')
def robots_txt():
    """Serves the robots.txt file for web crawlers."""
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: " + request.url_root.rstrip('/') + url_for('publico.sitemap') + "\n"
    )

@bp.route('/buscar')
def search_results():
    """
    Renders the search results page, searching both products and articles.
    """
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 9

    # --- ADD THIS DEBUG PRINT STATEMENT ---
    print(f"DEBUG: Search query received: '{query}'")
    # -------------------------------------

    productos_found = []
    articulos_found = []
    total_pages = 1

    if query:
        products_query = Producto.query.filter(
            (Producto.nombre.ilike(f'%{query}%')) |
            (Producto.descripcion.ilike(f'%{query}%'))
        )
        articles_query = Articulo.query.filter(
            (Articulo.titulo.ilike(f'%{query}%')) |
            (Articulo.contenido.ilike(f'%{query}%'))
        )

        productos_pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
        productos_found = productos_pagination.items

        # --- ADD THESE DEBUG PRINT STATEMENTS ---
        print(f"DEBUG: Found {len(productos_found)} products for query '{query}'")
        for p in productos_found:
            print(f"     - Product: {p.nombre} (ID: {p.id})")
        # -------------------------------------

        total_products_pages = productos_pagination.pages

        articulos_pagination = articles_query.paginate(page=page, per_page=per_page, error_out=False)
        articulos_found = articulos_pagination.items

        # --- ADD THESE DEBUG PRINT STATEMENTS ---
        print(f"DEBUG: Found {len(articulos_found)} articles for query '{query}'")
        for a in articulos_found:
            print(f"     - Article: {a.titulo} (ID: {a.id})")
        # -------------------------------------

        total_articles_pages = articulos_pagination.pages

        total_pages = max(total_products_pages, total_articles_pages) if productos_found or articulos_found else 1

    return render_template('search_results.html',
                           query=query,
                           productos=productos_found,
                           articulos=articulos_found,
                           page=page, # Corrected 'página=página,'
                           total_pages=total_pages)

### Affiliate User Interface and API Routes

@bp.route('/ref/<int:afiliado_id>')
def register_click(afiliado_id):
    afiliado = Afiliado.query.get_or_404(afiliado_id)

    estadistica = EstadisticaAfiliado.query.filter_by(
        afiliado_id=afiliado.id,
        fecha=date.today()
    ).first() # Corrected '.primero()'

    if estadistica:
        estadistica.clics += 1 # Assuming 'clics' is the correct attribute name in your model
    else: # Corrected 'más:'
        estadistica = EstadisticaAfiliado(
            afiliado_id=afiliado.id,
            clics=1, # Assuming 'clics' is the correct attribute name in your model
            fecha=date.today()
        )
        db.session.add(estadistica)

    db.session.commit()

    return redirect(afiliado.enlace_referido) # Ensure 'enlace_referido' is the correct attribute name for the affiliate URL in your Afiliado model