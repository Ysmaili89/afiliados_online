# C:\Users\joran\OneDrive\data\Documentos\LMSGI\afiliados_app\forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField, PasswordField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired, URL, NumberRange, Optional, Length, ValidationError, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from models import Producto, Afiliado # Removed AdsenseConfig as it's not directly used here

# ... (the rest of your forms.py content) ...
# Validador personalizado para rutas relativas o URLs completas
def validate_image_path(form, field):
    if field.data and not (
        field.data.startswith(('http://', 'https://', '/', 'static/'))
    ):
        raise ValidationError('La URL de la imagen debe comenzar con http://, https:// o ser una ruta válida (ej. /static/img/ o static/uploads/...).')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class ProductForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired(), Length(min=2, max=200)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0.01, message='El precio debe ser un número positivo.')])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    imagen = StringField('URL de la Imagen', validators=[Optional(), validate_image_path])
    link = StringField('Enlace de Afiliado', validators=[DataRequired(), URL(message='Por favor, introduce una URL válida.')])
    categoria_id = SelectField('Categoría', coerce=lambda x: int(x) if x else None, validators=[DataRequired(message='Por favor, selecciona una categoría.')])
    external_id = StringField('ID Externo (Opcional)', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Guardar Producto')

class CategoryForm(FlaskForm):
    nombre = StringField('Nombre de la Categoría', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Guardar Categoría')

class SubCategoryForm(FlaskForm):
    nombre = StringField('Nombre de la Subcategoría', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Guardar Subcategoría')

class ArticleForm(FlaskForm):
    titulo = StringField('Título del Artículo', validators=[DataRequired(), Length(min=5, max=200)])
    contenido = TextAreaField('Contenido del Artículo', validators=[DataRequired()])
    autor = StringField('Autor', validators=[Optional(), Length(max=100)])
    imagen = StringField('URL de la Imagen (Opcional)', validators=[Optional(), validate_image_path])
    submit = SubmitField('Guardar Artículo')

class ApiSyncForm(FlaskForm):
    api_url = StringField('URL de la API Externa', validators=[DataRequired(), URL(message='Por favor, introduce una URL válida para la API.')])
    submit = SubmitField('Sincronizar Productos')

class SocialMediaForm(FlaskForm):
    platform = SelectField('Plataforma', choices=[
        ('Facebook', 'Facebook'),
        ('Twitter', 'X (Twitter)'),
        ('Instagram', 'Instagram'),
        ('LinkedIn', 'LinkedIn'),
        ('YouTube', 'YouTube'),
        ('TikTok', 'TikTok'),
        ('WhatsApp', 'WhatsApp'),
        ('Telegram', 'Telegram'),
        ('Pinterest', 'Pinterest'),
        ('Snapchat', 'Snapchat'),
        ('Discord', 'Discord'),
        ('Reddit', 'Reddit'),
        ('Other', 'Otro')
    ], validators=[DataRequired()])
    url = StringField('URL del Perfil', validators=[DataRequired(), URL()])
    is_visible = BooleanField('Visible en el Sitio Público', default=True)
    submit = SubmitField('Guardar Enlace')

class ContactMessageAdminForm(FlaskForm):
    response_text = TextAreaField('Responder Mensaje', validators=[Optional()])
    is_read = BooleanField('Marcar como Leído', default=False)
    is_archived = BooleanField('Archivar Mensaje', default=False)
    submit_response = SubmitField('Enviar Respuesta y Actualizar')

class TestimonialForm(FlaskForm):
    author = StringField('Autor del Testimonio', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Contenido del Testimonio', validators=[DataRequired()])
    is_visible = BooleanField('Visible en el Sitio Público', default=False)
    likes = StringField('Likes (solo lectura)', render_kw={'readonly': True})
    dislikes = StringField('Dislikes (solo lectura)', render_kw={'readonly': True})
    submit = SubmitField('Guardar Testimonio')

class PublicTestimonialForm(FlaskForm):
    author = StringField('Tu Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Tu Testimonio', validators=[DataRequired(), Length(min=10, max=500)], render_kw={"rows": 5})
    fax_number = StringField('Número de Fax (no rellenar)', validators=[Optional()])  # Honeypot anti-spam
    submit = SubmitField('Enviar Testimonio')

class AdvertisementForm(FlaskForm):
    AD_TYPE_CHOICES = [
        ('destacado', 'Destacado (Texto/Botón)'),
        ('recomendado', 'Producto Recomendado'),
        ('mas_vendido', 'Lo Más Vendido (Texto/Botón)'),
        ('patrocinado', 'Patrocinado (AdSense)'),
        ('relevante', 'Relevante (AdSense)')
    ]

    type = SelectField('Tipo de Anuncio', choices=AD_TYPE_CHOICES, validators=[DataRequired()])
    title = StringField('Título del Anuncio', validators=[DataRequired(), Length(max=200)])
    is_active = BooleanField('Activo', default=True)

    text_content = TextAreaField('Contenido de Texto', validators=[Optional()])
    button_text = StringField('Texto del Botón', validators=[Optional(), Length(max=100)])
    button_url = StringField('URL del Botón', validators=[Optional(), URL()])

    product = QuerySelectField(
        'Producto Recomendado',
        query_factory=lambda: Producto.query.order_by(Producto.nombre).all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.nombre,
        allow_blank=True,
        blank_text='-- Selecciona un Producto --',
        validators=[Optional()]
    )
    image_url = StringField('URL de la Imagen (Producto Recomendado)', validators=[Optional(), validate_image_path])

    adsense_client_id = StringField('ID de Cliente AdSense (ca-pub-XXXXXXXXXXXXXX)', validators=[Optional(), Length(max=50)])
    adsense_slot_id = StringField('ID de Slot AdSense (9999999999)', validators=[Optional(), Length(max=50)])

    start_date = DateTimeLocalField('Fecha de Inicio (Opcional)', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    end_date = DateTimeLocalField('Fecha de Fin (Opcional)', format='%Y-%m-%dT%H:%M', validators=[Optional()])

    submit = SubmitField('Guardar Anuncio')

    def validate(self):
        # Always call the superclass validate method first
        if not super().validate():
            return False
        
        if self.type.data == 'recomendado':
            if not self.product.data and not self.image_url.data:
                msg = 'Debes seleccionar un producto o proporcionar una URL de imagen.'
                self.product.errors.append(msg)
                self.image_url.errors.append(msg)
                return False
        elif self.type.data in ['destacado', 'mas_vendido']:
            if not (self.text_content.data or self.button_text.data or self.button_url.data):
                self.text_content.errors.append('Para este tipo de anuncio, se requiere contenido de texto, texto del botón o URL del botón.')
                return False
        elif self.type.data in ['patrocinado', 'relevante']:
            if not self.adsense_client_id.data or not self.adsense_slot_id.data:
                msg = 'Se requieren el ID de Cliente y el ID de Slot de AdSense para este tipo de anuncio.'
                self.adsense_client_id.errors.append(msg)
                self.adsense_slot_id.errors.append(msg)
                return False
        
        if self.start_date.data and self.end_date.data and self.start_date.data >= self.end_date.data:
            self.end_date.errors.append('La fecha de fin debe ser posterior a la fecha de inicio.')
            return False

        return True

# -----------------------------------------------------------------------------
# Formularios de afiliados (Movido de admin.py para arreglar F811)
# -----------------------------------------------------------------------------

class AffiliateForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120), Email()])
    enlace_referido = StringField('Enlace de Referido', validators=[DataRequired(), URL()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Afiliado')

class AffiliateStatisticForm(FlaskForm):
    start_date = DateTimeLocalField('Fecha de Inicio', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    end_date = DateTimeLocalField('Fecha de Fin', format='%Y-%m-%dT%H:%M', validators=[Optional()])

    afiliado = QuerySelectField(
        'Afiliado',
        query_factory=lambda: Afiliado.query.order_by(Afiliado.nombre).all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.nombre,
        allow_blank=True, # Corrected 'Verdadero' to 'True'
        blank_text='-- Todos los Afiliados --',
        validators=[Optional()] # Corrected 'validadores=[Opcional()]' to 'validators=[Optional()]'
    )
    submit = SubmitField('Generar Reporte')

# -----------------------------------------------------------------------------
# Nuevo: Formulario de configuración de Adsense
# -----------------------------------------------------------------------------
class AdsenseConfigForm(FlaskForm): # Corrected 'clase' to 'class'
    # Estos campos deben coincidir con los atributos de su modelo AdsenseConfig
    client_id = StringField('ID de Cliente AdSense (data-ad-client)', validators=[DataRequired(), Length(max=50)])
    ad_slot_header = StringField('ID de Slot para Encabezado', validators=[Optional(), Length(max=50)])
    ad_slot_sidebar = StringField('ID de Slot para Barra Lateral', validators=[Optional(), Length(max=50)])
    ad_slot_article_top = StringField('ID de Slot para Cima de Artículo', validators=[Optional(), Length(max=50)])
    ad_slot_article_bottom = StringField('ID de Slot para Pie de Artículo', validators=[Optional(), Length(max=50)])
    is_active = BooleanField('Activar AdSense', default=False)
    submit = SubmitField('Guardar Configuración AdSense')