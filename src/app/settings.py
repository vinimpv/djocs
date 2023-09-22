from pathlib import Path
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "umhg)27ulh6&+7x&+*!!$io136u%k3pt(%b938%68p+4$(vj75"
DEBUG = True
ALLOWED_HOSTS: list[str] = []
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "app.core",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "compressor",
    "django_htmx",
    "django_extensions",
    "simple_history",
    "django_summernote",
    "storages",
    "django_browser_reload",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "app.wsgi.application"

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


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


COMPRESS_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
STATICFILES_FINDERS = (
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://postgres:postgres@postgres:5432/postgres",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

DJOCS_EMBEDDING_MODEL = "text-embedding-ada-002"
DJOCS_GPT_MODEL = "gpt-3.5-turbo"

DJOCS_MAX_PROMPT_TOKENS = 4000
DJOCS_MAX_KNOWLEDGE_TOKENS = 1000
DJOCS_HISTORY_KNOWLEDGE_RATIO = 0.5

LOGIN_REDIRECT_URL = "/"
