import hashlib
import os
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = str(BASE_DIR.joinpath("media"))
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


def clean_hosts(val):
    if isinstance(val, list):
        return [item.strip() for item in val]
    elif isinstance(val, str):
        return [s.strip() for s in val.strip("'\"").split(",")]
    else:
        raise TypeError(
            f"hosts must be a list or comma separated string not {type(val)}"
        )


# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = config("SECRET_KEY")  # Default secret_key generated in entrypoint.sh
USER_ID = hashlib.md5(SECRET_KEY.encode()).hexdigest()
DEBUG = config("DEBUG", default=False, cast=bool)
TEMPLATE_DEBUG = config("TEMPLATE_DEBUG", default=DEBUG, cast=bool)

SERVER_HOST = config("SERVER_HOST", default="localhost", cast=str)
SERVER_PORT = config("SERVER_PORT", default="8000", cast=str)
FRONTEND_HOST = config("FRONTEND_HOST", default=SERVER_HOST, cast=str)
FRONTEND_PORT = config("SERVER_PORT", default="3000", cast=str)

DISABLE_HTTP = config("DISABLE_HTTP", default=False)

schemes = ["https"] if DISABLE_HTTP else ["http", "https"]
hosts = {SERVER_HOST, FRONTEND_HOST}
if DEBUG:
    default_allowed_hosts = ["*"]
    default_csrf_trusted_origins = [f"{scheme}://*" for scheme in schemes]
    default_cors_allowed_origins = default_csrf_trusted_origins
    default_allow_all_origins = True
else:
    default_allowed_hosts = [SERVER_HOST, "127.0.0.1", "[::1]"]
    default_csrf_trusted_origins = [
        f"{scheme}://{host}" for scheme in schemes for host in hosts
    ]
    default_cors_allowed_origins = [
        f"{scheme}://{host}"
        for scheme in schemes
        for host in [FRONTEND_HOST, f"{FRONTEND_HOST}:{FRONTEND_PORT}"]
    ]
    default_allow_all_origins = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=default_allowed_hosts, cast=clean_hosts)
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default=default_cors_allowed_origins, cast=clean_hosts
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", default=default_csrf_trusted_origins, cast=clean_hosts
)
CORS_ALLOW_ALL_ORIGINS = config(
    "CORS_ALLOW_ALL_ORIGINS", default=default_allow_all_origins, cast=bool
)


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
    "strawberry.django",
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
    "connections",
    "workspaces",
    "users",
    "telemetry",
]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + THE_GUIDE_APPS

MIDDLEWARE = [
    "middleware.HealthCheckMiddleware.HealthCheckMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middleware.MultitenantMiddleware.MultitenantMiddleware",
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
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/tmp/debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
