from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = bool(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(" ")
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #3rd party packs
    "crispy_forms",
    "crispy_tailwind",
    'django_admin_generator',
    'import_export',
    'login_history',
    'easyaudit',
    'compressor',
    'rest_framework',
    # my app
    "accounts.apps.AccountsConfig",
    "orders.apps.OrdersConfig",
    "django_htmx",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'accounts.middleware.OneSessionPerUserMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'project.wsgi.application'


# The compressor of Tailwind
COMPRESS_ROOT = BASE_DIR / 'staticfiles'
COMPRESS_ENABLED = True
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 80,  # Set timeout to 20 seconds
#         },
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("P_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("P_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("P_USER", "user"),
        "PASSWORD": os.environ.get("P_PASSWORD", "password"),
        "HOST": os.environ.get("P_HOST", "localhost"),
        "PORT": os.environ.get("P_PORT", "5432"),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'vision_db',
#         'USER': 'alien',
#         'PASSWORD': 'AAsd01203394542',
#         'HOST': 'vision-1.cj2g2i08e29f.eu-north-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login & logout redirection
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

#crispy settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# auto logout
AUTO_LOGOUT = {
    'IDLE_TIME': 600,
    'MESSAGE': 'The session has expired. Please login again to continue.',
}
