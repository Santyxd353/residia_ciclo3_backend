import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad / entorno ---
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
DEBUG = os.getenv('DEBUG', '1') == '1'

# hostnames permitidos en dev
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', '0.0.0.0']

# --- Apps ---
INSTALLED_APPS = [
    
    'rest_framework',
    'rest_framework_simplejwt',   # <- añade esto
    'corsheaders',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

  
    'users',
    'units',
    'residents',
    'vehicles',
    'announcements',
    'finance',
    'bookings',
    'incidents',
    'visitors',
    'security',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Middleware (CORS primero) ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # <- debe ir arriba
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Admin usa CSRF; API va con JWT
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'residia.urls'

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

WSGI_APPLICATION = 'residia.wsgi.application'

# --- DB ---
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'residia'),
        'USER': os.getenv('DB_USER', 'residia'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'residia'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {'sslmode': 'require'},  # <-- AÑADE ESTO
    }
}



# --- Passwords ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# --- DRF / JWT ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # API
        'rest_framework.authentication.SessionAuthentication',        # Admin
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

from rest_framework.settings import api_settings  # solo para evitar warnings en algunos editores

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),   # <- importante para "Authorization: Bearer <token>"
}

# --- CORS / CSRF para frontend local (Vite) ---
CORS_ALLOW_CREDENTIALS = True

# Si quieres ir a lo seguro en dev, abre CORS para todo:
CORS_ALLOW_ALL_ORIGINS = True

# Si prefieres lista explícita, comenta la línea de arriba y usa esto:
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:5173',
#     'http://127.0.0.1:5173',
# ]

# Encabezados habituales
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',   # <- necesario para Bearer token
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Para evitar problemas con CSRF en admin cuando entras desde Vite/localhost
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
