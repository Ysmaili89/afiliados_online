import pytest
from app import app, db, User, Product, Category, Article
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        # Crear categoría primero porque Product depende de category_id
        category = Category(name='Test Category', slug='test-category')
        db.session.add(category)
        db.session.commit()  # Necesario para obtener el id de category

        # Crear usuarios con password hash generado correctamente
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('userpass'),
            is_admin=False
        )
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('adminpass'),
            is_admin=True
        )

        product = Product(
            name='Test Product',
            slug='test-product',
            price='$100',
            description='A test product.',
            link='http://test.com',
            category_id=category.id
        )

        # Nota: En Article el campo fecha es string, aquí asignamos con formato ISO
        article = Article(
            titulo='Test Article',
            slug='test-article',
            contenido='Content of test article.',
            autor='Test Author',
            fecha='2024-01-01'
        )

        db.session.add_all([user, admin_user, product, article])
        db.session.commit()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


def login(client, username, password):
    return client.post('/admin/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/admin/logout', follow_redirects=True)


def test_index_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Productos Destacados" in rv.data


def test_admin_login_logout(client):
    rv = login(client, 'admin', 'adminpass')
    assert b"Inicio de sesi\xc3\xb3n exitoso como administrador." in rv.data
    assert b"Panel de administraci\xc3\xb3n" in rv.data

    rv = logout(client)
    assert b"Has cerrado sesi\xc3\xb3n." in rv.data
    assert b"Login" in rv.data

    rv = login(client, 'admin', 'wrongpassword')
    assert b"Nombre de usuario o contrase\xc3\xb1a incorrectos." in rv.data


def test_product_detail_page(client):
    rv = client.get('/product/test-product')
    assert rv.status_code == 200
    assert b"Test Product" in rv.data


def test_non_existent_product(client):
    rv = client.get('/product/non-existent')
    assert b"Producto no encontrado." in rv.data
    assert rv.status_code == 200


def test_categories_page(client):
    rv = client.get('/categorias')
    assert rv.status_code == 200
    assert b"Explorar Categor\xc3\xadas" in rv.data
    assert b"Test Category" in rv.data


def test_articles_page(client):
    rv = client.get('/guias')
    assert rv.status_code == 200
    assert b"Gu\xc3\xadas y Art\xc3\xadculos Especializados" in rv.data
    assert b"Test Article" in rv.data


def test_admin_dashboard_access(client):
    rv = client.get('/admin/dashboard')
    # Asegúrate que la app redirige a login o muestra mensaje de sesión requerida
    assert b"Por favor, inicia sesi\xc3\xb3n para acceder a esta p\xc3\xa1gina." in rv.data or rv.status_code in (302, 401, 403)

    login(client, 'admin', 'adminpass')
    rv = client.get('/admin/dashboard')
    assert rv.status_code == 200
    assert b"Resumen del Panel de Administraci\xc3\xb3n" in rv.data
    logout(client)


