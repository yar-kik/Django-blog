from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = ["kotolampa.live", "127.0.0.1", "localhost"]

DEBUG = False

INSTALLED_APPS = [
    "authentication",
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
    "django.contrib.postgres",
    "rest_framework",
    "social_django",
    "sorl.thumbnail",
    "phonenumber_field",
    "imagekit",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "postgres"),
        "USER": os.environ.get("DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "postgres"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "CONN_MAX_AGE": 60,
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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATIC_ROOT = os.path.join(BASE_DIR, "../../static/")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
