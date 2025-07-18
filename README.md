Afiliados App (Flask)
Descripción:
Aplicación web para afiliados construida con Flask que muestra productos destacados, guías de compra y comparativas para facilitar decisiones informadas.

🧩 Características Principales
✅ Página de Inicio: Productos destacados y secciones relevantes.

🛠️ Gestión de Productos: CRUD completo (Crear, Leer, Actualizar, Borrar) con enlaces de afiliado, descripciones, precios e imágenes.

🗂️ Categorías y Subcategorías: Organización jerárquica de productos.

📚 Guías y Artículos: Publicación de contenido especializado para usuarios.

🔐 Panel de Administración: Acceso protegido con autenticación.

📄 Páginas Informativas: Contacto, Política de Privacidad, Términos y Condiciones, Cookies.

📈 SEO Amigable: Sitemap y robots.txt generados dinámicamente.

📱 Diseño Responsivo con Bootstrap 5.3.

🎨 Modo Oscuro: Alternancia entre tema claro y oscuro.

🌍 Widget de Traducción de Google para idiomas automáticos.

⭐ Iconografía con Font Awesome 6.5.

🔄 Sincronización API (opcional): Posibilidad de sincronizar productos desde una API externa configurable.

⚙️ Instalación y Ejecución Local
Clona el repositorio

bash
Copiar
Editar
git clone https://github.com/Ysmaili89/afiliados_online.git
cd afiliados_app
Crea y activa un entorno virtual (opcional pero recomendado)

bash
Copiar
Editar
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / MacOS
source venv/bin/activate
Instala las dependencias

bash
Copiar
Editar
pip install -r requirements.txt
Configura variables de entorno (ejemplo):

FLASK_APP=app.py

FLASK_ENV=development

Configura claves API o base de datos si aplica.

Ejecuta la aplicación

bash
Copiar
Editar
flask run
Abre tu navegador en http://127.0.0.1:5000

📂 Estructura del Proyecto
/app.py: Archivo principal de la aplicación Flask.

/migrations: Scripts para migraciones de base de datos.

/routes: Definición de rutas de la app.

/services: Lógica de negocio y servicios externos.

/static: Archivos estáticos (CSS, JS, imágenes).

/templates: Plantillas HTML de Jinja2.

/config.py: Configuraciones de la app.

/models.py: Modelos de datos (ORM).

/forms.py: Formularios WTForms para la app.

/extensions.py: Inicialización de extensiones Flask.

/utils.py: Funciones auxiliares.

requirements.txt: Dependencias del proyecto.

📝 Funcionalidades Adicionales
Sincronización automática desde API externa (configurable).

Panel de administración con autenticación y roles.

Gestión completa de productos, categorías, subcategorías y artículos.

Sistema SEO dinámico para mejorar posicionamiento.

Diseño responsivo y accesible.

Modo oscuro para mejor experiencia de usuario.