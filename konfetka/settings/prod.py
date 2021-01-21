from .settings import *

ALLOWED_HOSTS = ['kotolampa.live']

DEBUG = False

INSTALLED_APPS = [
    'account',
    'articles',
    'archives',

    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'taggit',
    'social_django',
    'sorl.thumbnail',
    'phonenumber_field',
    'django.contrib.postgres',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'environ',
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

STATIC_ROOT = os.path.join(BASE_DIR, '../../static/')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
