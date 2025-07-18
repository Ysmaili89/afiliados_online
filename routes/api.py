# C:\Users\joran\OneDrive\data\Documentos\LMSGI\afiliados_app\routes\api.py

from flask import Blueprint, jsonify # Removed 'request' as it's not used in this file
# Removed 'from app import db' as 'db' is not directly used in this file's queries
from models import Producto, Categoria, Subcategoria, Articulo # Ensure Subcategoria is imported explicitly
from sqlalchemy.orm import joinedload # To efficiently load related data

bp = Blueprint('api', __name__, url_prefix='/api')

# Get all products
@bp.route('/productos', methods=['GET'])
def api_productos():
    productos = Producto.query.all()
    productos_data = [{
        "id": p.id,
        "nombre": p.nombre,
        "slug": p.slug,
        "precio": p.precio,
        "descripcion": p.descripcion,
        "imagen": p.imagen,
        "link": p.link,
        "subcategoria_id": p.subcategoria_id,
        "external_id": p.external_id,
        "fecha_creacion": p.fecha_creacion.isoformat() if p.fecha_creacion else None,
        "fecha_actualizacion": p.fecha_actualizacion.isoformat() if p.fecha_actualizacion else None
    } for p in productos]
    return jsonify(productos_data)

# Get a product by ID
@bp.route('/productos/<int:producto_id>', methods=['GET'])
def api_producto_por_id(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        return jsonify({
            "id": producto.id,
            "nombre": producto.nombre,
            "slug": producto.slug,
            "precio": producto.precio,
            "descripcion": producto.descripcion,
            "imagen": producto.imagen,
            "link": producto.link,
            "subcategoria_id": producto.subcategoria_id,
            "external_id": producto.external_id,
            "fecha_creacion": producto.fecha_creacion.isoformat() if producto.fecha_creacion else None,
            "fecha_actualizacion": producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
        })
    return jsonify({"mensaje": "Producto no encontrado"}), 404

# Get all categories
@bp.route('/categorias', methods=['GET'])
def api_categorias():
    categorias = Categoria.query.all()
    categorias_data = [{
        "id": c.id,
        "nombre": c.nombre,
        "slug": c.slug
    } for c in categorias]
    return jsonify(categorias_data)

# Get a category by ID with its subcategories
@bp.route('/categorias/<int:categoria_id>', methods=['GET'])
def api_categoria_por_id(categoria_id):
    # Use joinedload to prevent N+1 query problem for subcategories
    categoria = Categoria.query.options(joinedload(Categoria.subcategorias)).get(categoria_id)
    if categoria:
        subcategorias_data = [{
            "id": sc.id,
            "nombre": sc.nombre,
            "slug": sc.slug,
            "categoria_id": sc.categoria_id
        } for sc in categoria.subcategorias]
        return jsonify({
            "id": categoria.id,
            "nombre": categoria.nombre,
            "slug": categoria.slug,
            "subcategorias": subcategorias_data
        })
    return jsonify({"mensaje": "Categoría no encontrada"}), 404

# Get all subcategories (New endpoint, useful for nested relationships)
@bp.route('/subcategorias', methods=['GET'])
def api_subcategorias():
    subcategorias = Subcategoria.query.all()
    subcategorias_data = [{
        "id": sc.id,
        "nombre": sc.nombre,
        "slug": sc.slug,
        "categoria_id": sc.categoria_id
    } for sc in subcategorias]
    return jsonify(subcategorias_data)

# Get a subcategory by ID with its products (New endpoint)
@bp.route('/subcategorias/<int:subcategoria_id>', methods=['GET'])
def api_subcategoria_por_id(subcategoria_id):
    subcategoria = Subcategoria.query.options(joinedload(Subcategoria.productos)).get(subcategoria_id)
    if subcategoria:
        productos_data = [{
            "id": p.id,
            "nombre": p.nombre,
            "slug": p.slug,
            "precio": p.precio,
            "imagen": p.imagen,
            "link": p.link
        } for p in subcategoria.productos]
        return jsonify({
            "id": subcategoria.id,
            "nombre": subcategoria.nombre,
            "slug": subcategoria.slug,
            "categoria_id": subcategoria.categoria_id,
            "productos": productos_data
        })
    return jsonify({"mensaje": "Subcategoría no encontrada"}), 404


# Get all articles
@bp.route('/articulos', methods=['GET'])
def api_articulos():
    articulos = Articulo.query.all()
    articulos_data = [{
        "id": a.id,
        "titulo": a.titulo,
        "slug": a.slug, # Corrected: Added slug field
        "contenido": a.contenido,
        "autor": a.autor, # Corrected: 'Autor' to 'autor'
        "fecha": a.fecha.isoformat() if a.fecha else None,
        "imagen": a.imagen
    } for a in articulos]
    return jsonify(articulos_data)

# Obtener un artículo por ID
@bp.route('/articulos/<int:articulo_id>', methods=['GET'])
def api_articulo_por_id(articulo_id):
    articulo = Articulo.query.get(articulo_id)
    if articulo:
        return jsonify({
            "id": articulo.id,
            "titulo": articulo.titulo,
            "slug": articulo.slug,
            "contenido": articulo.contenido,
            "autor": articulo.autor,
            "fecha": articulo.fecha.isoformat() if articulo.fecha else None,
            "imagen": articulo.imagen
        })
    return jsonify({"mensaje": "Artículo no encontrado"}), 404