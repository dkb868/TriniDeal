"""
Django settings for manicou project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#relative paths
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%p+yi&ibzu&6&xv0_f&5p2mj&zz_%b=75jm8dtm5@v@^*0m(d)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


#Template directory

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',

    # review apps
    'hvad',
    'review',
    'user_media',
    'generic_positions',


    # allauth apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    # noticiation app
    'notifications',

    # contact form
    'envelope',
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'manicou.urls'

WSGI_APPLICATION = 'manicou.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Port_of_Spain'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

#Media files, uploaded images etc.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Allauth stuff

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk',
        'LOCALE_FUNC': lambda request: 'en_GB',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.2'}}

LOGIN_REDIRECT_URL = '/'

ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_FORM_CLASS = 'shop.forms.SignupForm'

# Review stuff

REVIEW_UPDATE_SUCCESS_URL = 'index'
REVIEW_ALLOW_ANONYMOUS = False


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'support@trinideal.com'
EMAIL_HOST_USER = 'support@trinideal.com'
EMAIL_HOST_PASSWORD = 'Allthatiknow1'

# contact

ENVELOPE_EMAIL_RECIPIENTS = ['support@trinideal.com','mitrikyle@yahoo.com']