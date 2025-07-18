import os

class Config:
    # The SECRET_KEY is crucial for Flask and Flask-Login security.
    # It MUST be an environment variable in production.
    # In development, you can set it in your .env file
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_por_defecto_solo_para_desarrollo_local'
    
    # WARNING! Do not use SQLite in production for large or concurrent relational databases.
    # PostgreSQL, MySQL, etc., are recommended.
    # For production, you would configure something like:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@host/db_name'
    # For development, you can use SQLite:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Corrected 'Falso' to 'False'

    # Other configurations you might need:
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True # Corrected 'Verdadero' to 'True'
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')