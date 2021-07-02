import os
from .settings import BASE_DIR

ALLOWED_HOSTS = ["kotolampa.live", "127.0.0.1", "localhost"]

DEBUG = False

INSTALLED_APPS = [
    "account",
    "articles",
    "archives",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "social_django",
    "sorl.thumbnail",
    "phonenumber_field",
    "django.contrib.postgres",
    "ckeditor",
    "ckeditor_uploader",
    "imagekit",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATIC_ROOT = os.path.join(BASE_DIR, "../../static/")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
