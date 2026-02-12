import os
from pathlib import Path
import dj_database_url

# =====================
# Chemin de base du projet
# =====================
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# Clés et Debug
# =====================
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-defaultkey")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]  # Sur Render, "*" suffit pour tester, sinon mets ton domaine

# =====================
# Applications
# =====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Pour formatage humain
    'core',  # Ton application principale
]

# =====================
# Middleware
# =====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurantplus.urls'

# =====================
# Templates
# =====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'restaurantplus.wsgi.application'

# =====================
# Base de données (Render / DATABASE_URL)
# =====================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# =====================
# Validation des mots de passe
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =====================
# Internationalisation
# =====================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = os.environ.get('TIME_ZONE', 'Africa/Abidjan')
USE_I18N = True
USE_TZ = True

# =====================
# Fichiers statiques et médias
# =====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =====================
# Autres
# =====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
