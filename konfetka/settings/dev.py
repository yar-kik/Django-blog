from .settings import *

ALLOWED_HOSTS = ["localhost",
                 "127.0.0.1"]
INSTALLED_APPS = [
    'account',
    'articles',
    'archives',

    'dal',
    'dal_select2',
    "livereload",

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
    'debug_toolbar',
    'django.contrib.postgres',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'environ',
]
DEBUG = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'livereload.middleware.LiveReloadScript',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../static"),
]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
