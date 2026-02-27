
from os.path import dirname, exists, join
from pathlib import Path

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_file = join(dirname(__file__), 'local.env')
if exists(env_file):
    environ.Env.read_env(str(env_file))

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'drf_spectacular',
    'rest_framework',
    'rest_framework.authtoken',

    # Project apps
    'apps.accounts',
    'apps.audit'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

REST_FRAMEWORK = {
    'DATE_FORMAT': '%d-%m-%Y',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
            'djangorestframework_camel_case.parser.CamelCaseFormParser',
            'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
            'djangorestframework_camel_case.parser.CamelCaseJSONParser',
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ],
    'DEFAULT_RENDERER_CLASSES': [
                'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
                'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
                'rest_framework.renderers.JSONRenderer',
                'rest_framework.renderers.BrowsableAPIRenderer',
            ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'JSON_UNDERSCOREIZE': {
            'no_underscore_before_number': True
        },
}


WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_EMAIL = 'The TSES Team'


SPECTACULAR_SETTINGS = {
    'TITLE': 'TSES API',
    'DESCRIPTION': 'Django API sample project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CAMELIZE_NAMES': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'AUTHENTICATION_WHITELIST': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'POSTPROCESSING_HOOKS': [
            'drf_spectacular.hooks.postprocess_schema_enums',
            'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields'
        ],
    'COMPONENT_SPLIT_REQUEST': True,
}