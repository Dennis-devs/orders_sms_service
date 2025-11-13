
from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url
from google.cloud import secretmanager

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'SEC')
DEBUG = os.getenv('DJANGO_ENV', 'development') == 'development'

ALLOWED_HOSTS = f'{os.getenv('ALLOWED_HOSTS')},localhost,127.0.0.1'.split(',')

# Production Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'orders_mgmt',
    'rest_framework',
    'mozilla_django_oidc',
]
AUTHENTICATION_BACKENDS = (
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)

OIDC_AUTH0_DOMAIN = os.getenv('OIDC _AUTH0_DOMAIN')
OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET')
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://dev-qlfgtecl6j1fbku7.us.auth0.com/authorize'
OIDC_OP_TOKEN_ENDPOINT = 'https://dev-qlfgtecl6j1fbku7.us.auth0.com/oauth/token'
OIDC_OP_USER_ENDPOINT = 'https://dev-qlfgtecl6j1fbku7.us.auth0.com/userinfo'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_OP_JWKS_ENDPOINT = 'https://dev-qlfgtecl6j1fbku7.us.auth0.com/.well-known/jwks.json'
OIDC_REDIRECT_URL = 'http://localhost:8000/oidc/callback/'
OIDC_OP_LOGOUT_URL = 'dev-qlfgtecl6j1fbku7.us.auth0.com/v2/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/oidc/authenticate/'

AFRICASTALKING_USERNAME = 'sandbox'
AFRICASTALKING_API_KEY = os.getenv('AFRICASTALKING_API_KEY')
MESSAGING_URL = os.getenv('AFRICASTALKING_MESSAGING_URL')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.UserRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'user': '100/hour'}
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
]


ROOT_URLCONF = 'orders_sms_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'orders_sms_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if not DEBUG:
    database_url = os.environ.get('DATABASE_URL')
    print("Production database URL:", database_url)  # Debugging line
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# def get_secret_value(secret_id, project_id="sms-service-474413"):
#     """Fetches a secret from Secret Manager."""
#     try:
#         client = secretmanager.SecretManagerServiceClient()
#         name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
#         response = client.access_secret_version(name=name)
#         return response.payload.data.decode('UTF-8')
#     except Exception as e:
#         # Handling error appropriately (e.g., fallback or raise)
#         print(f"Failed to fetch secret '{secret_id}': {e}")
#         return None

# # Check if running on Google Cloud App Engine
# if os.getenv('GAE_APPLICATION') or os.getenv('GAE_ENV') == 'standard':
#     # Production settings on App Engine
#     project_id = "sms-service-474413"

#     # Fetch all secrets before building the DATABASE_URL
#     db_user = get_secret_value("DB_USER", project_id)
#     db_pass = get_secret_value("DB_PASS", project_id)
#     db_name = get_secret_value("DB_NAME", project_id)
#     instance_connection_name = get_secret_value("INSTANCE_CONNECTION_NAME", project_id)

#     database_url = f"postgresql://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{instance_connection_name}"

#     # Configuration for App Engine
#     DATABASES = {
#         'default': dj_database_url.parse(
#             database_url,
#             conn_max_age=600,
#             ssl_require=False
#         )
#     }

#     SECRET_KEY = get_secret_value("DJANGO_SECRET_KEY", project_id)
#     ALLOWED_HOSTS = get_secret_value("ALLOWED_HOSTS", project_id).split(',')
# else:
#     # Fallback for local development
#     DATABASES = {
#         'default': dj_database_url.config(
#             default='sqlite:////app/db.sqlite3',
#             conn_max_age=600,
#         )
#     }

#     SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'SEC')
#     ALLOWED_HOSTS = f'{os.getenv('ALLOWED_HOSTS')},localhost,127.0.0.1'.split(',')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {'': {'handlers': ['console'], 'level': 'INFO'}},
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# For development only
STATIC_DIRS = [
    BASE_DIR / 'static'
]


# if os.getenv('GAE_APPLICATION'):
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# else:
#     STATICFILES_STORAGE = {
#         "staticfiles": {
#             "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#         },
#     }

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}