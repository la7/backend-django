# Configuración principal de Django
# Archivo regenerado correctamente
import os
from pathlib import Path

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad (Cambiar en producción)
SECRET_KEY = 'django-insecure-key-reemplazar-en-produccion'
DEBUG = True
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Bibliotecas de terceros
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    
    # Aquí irán tus apps cuando las agrupes (ej: 'apps.users', 'apps.products')
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Como tu urls.py está en la raíz, le indicamos a Django que lo busque ahí
ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Base de datos por defecto de Django (SQLite para admin/auth de Django)
# Nota: Tus servicios de MongoDB seguirán usando pymongo tal como los tienes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Swagger / Redoc
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Backend API',
    'DESCRIPTION': 'Documentación interactiva',
    'VERSION': '1.0.0',
}
