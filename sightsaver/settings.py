"""
Django settings for sightsaver project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os 
import environ 
from datetime import timedelta
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =os.getenv('SECRET_KEY') 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['sightsaver.onrender.com','localhost','127.0.0.1'] # add ngrok domain : ngrok http http://localhost:8000


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External app 
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'djoser',
    'rest_framework_simplejwt',
    # Internal app
    'accounts.apps.AccountsConfig',
    'payment.apps.PaymentConfig',
    'reservations.apps.ReservationsConfig',
    'chat.apps.ChatConfig',
    'cataract.apps.CataractConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
#        
# }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


DESCRIPTION = """Documentation of API endpoints of Sight Saver application.

Handle Error Codes:
```json
    400: "Bad request.",
    401: "Unauthorized.",
    404: "Not found.",
    405: "Method not allowed.",
    500: "Internal server error.",
    200: "OK.",
    201: "Created.",
    202: "Accepted.",
```

"""


SPECTACULAR_SETTINGS = {
    'TITLE':'SIGHT SAVER API DOCUMENTATION',
    'DESCRIPTION': DESCRIPTION ,
    'SERVE_PERMISSIONS': ["rest_framework.permissions.AllowAny"],

}


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',), #'JWT'
    'ACCESS_TOKEN_LIFETIME': timedelta(days=350),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=350),

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}




CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Authorization',
    'Content-Type',
]

ROOT_URLCONF = 'sightsaver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # i do not add the template url 
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

WSGI_APPLICATION = 'sightsaver.wsgi.application'

STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
print(DEBUG)
if (DEBUG == 'True'):
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
    }

else :
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    DATABASES = {
    'default': dj_database_url.parse(os.getenv("DATABASE_URL"))
    
    }



# Email configration for deployment
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# # Email configration for development
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST='sandbox.smtp.mailtrap.io'
# EMAIL_HOST_USER='60972b6568b304'
# EMAIL_HOST_PASSWORD='df8d09b7f05117'
# EMAIL_PORT=2525
# DEFAULT_FROM_EMAIL = "alyaa@backend.com"
# DOMAIN ='localhost:8000' # domain for the front end ,but i put 8000 not 5173 
# SITE_NAME = "Depressed Backend "  # ^_^
# DOMAIN='localhost:8000'


# payment  

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_KEY = os.getenv('STRIPE_WEBHOOK_KEY') # local key is different from the global
                     
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # will be used in production to store static files 
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# MEDIA_URL = 'media/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'
