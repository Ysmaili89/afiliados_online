import re
from unicodedata import normalize
from werkzeug.security import generate_password_hash
from models import User
from extensions import db

def slugify(text):
    """
    Convierte el texto en un slug compatible con URL.
    """
    if not isinstance(text, str): # Corrected 'si no isinstance(text, str):' to 'if not isinstance(text, str):'
        return "" # Corrected 'devolución ""' to 'return ""'
    # Normalizar caracteres Unicode para letras acentuadas, etc.
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Reemplace los caracteres no alfanuméricos con guiones
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    # Reemplace espacios y guiones múltiples con un solo guión
    text = re.sub(r'[-\s]+', '-', text)
    return text # Corrected 'Texto de retorno' to 'return text'

def _create_initial_data(app): # Corrected 'aplicación' to 'app'
    """
    Crea un usuario administrador inicial si no existe.
    """
    with app.app_context():
        if not User.query.filter_by(username='admin').first(): # Corrected 'si no User.query.filter_by(nombredeusuario='admin').first():' to 'if not User.query.filter_by(username='admin').first():'
            admin_user = User( # Corrected 'Usuario' to 'User'
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                is_admin=True # Corrected 'is_admin=Verdadero' to 'is_admin=True'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✔ Usuario administrador creado.")
        else: # Corrected 'más:' to 'else:'
            print("ℹ️ Usuario administrador ya existe.")