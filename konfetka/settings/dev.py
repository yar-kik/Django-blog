import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentication.middlewares.UserActivityMiddleware",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../static"),
]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
