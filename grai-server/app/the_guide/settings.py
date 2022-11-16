import os
from itertools import product
from pathlib import Path

from decouple import config
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = str(BASE_DIR.joinpath("media"))
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# SECURITY WARNING: keep the secret key used in production secret!


def clean_hosts(val):
    if isinstance(val, list):
        return [item.strip() for item in val]
    elif isinstance(val, str):
        return [s.strip() for s in val.split(",")]
    else:
        raise TypeError(f"hosts must be a list or a string not {type(val)}")


SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())
DEBUG = config("DEBUG", default=False, cast=bool)
TEMPLATE_DEBUG = config("TEMPLATE_DEBUG", default=DEBUG, cast=bool)

SERVER_HOST = config("SERVER_HOST", default="localhost", cast=str)
SERVER_PORT = config("SERVER_PORT", default="8000", cast=str)

FRONTEND_HOST = config("FRONTEND_HOST", default=SERVER_HOST, cast=str)
FRONTEND_PORT = config("FRONTEND_PORT", default="3000", cast=str)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=clean_hosts)
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default=[], cast=clean_hosts)
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default=[], cast=clean_hosts)

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = ["http://*", "https://*"]
else:
    schemes = ["http", "https"]
    default_ports = [SERVER_PORT, FRONTEND_PORT]
    default_hosts = list(set([SERVER_HOST, FRONTEND_HOST]))
    default_cors_origins = [
        f"{scheme}://{host}:{port}"
        for scheme, host, port in product(schemes, default_hosts, default_ports)
    ]

    default_csrf_origins = [
        f"{scheme}://{host}" for scheme in schemes for host in default_hosts
    ]

if not CORS_ALLOW_ALL_ORIGINS and not CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = default_cors_origins

if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = default_csrf_origins

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost"]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="grai"),
        "USER": config("DB_USER", default="grai"),
        "PASSWORD": config("DB_PASSWORD", default="grai"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}


DJANGO_CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "whitenoise.runserver_nostatic",
    # "strawberry.django",
    "rest_framework",
    "phonenumber_field",
    "corsheaders",
    "social_django",
    "rest_framework_simplejwt",
    "django_extensions",
    "rest_framework.authtoken",
    "rest_framework_api_key",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
]

THE_GUIDE_APPS = [
    "lineage",
    "users",
    "namespaces",
    "telemetry",
]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + THE_GUIDE_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ROOT_URLCONF = "the_guide.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "the_guide.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"


# https://nixhive.com/how-to-run-django-on-a-subpath-via-proxy/
# FORCE_SCRIPT_NAME = '/guide'
# USE_X_FORWARDED_HOST = True

PHONENUMBER_DEFAULT_REGION = "US"

# Https

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# OpenApi
# https://drf-spectacular.readthedocs.io/en/latest/settings.html

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'handlers': {
      'file': {
         'level': 'DEBUG',
         'class': 'logging.FileHandler',
         'filename': '/tmp/debug.log',
      },
   },
   'loggers': {
      'django': {
         'handlers': ['file'],
         'level': 'DEBUG',
         'propagate': True,
      },
   },
}