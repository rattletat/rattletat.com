"""
Base settings to build other settings files upon.
"""
from pathlib import Path
from django.utils.translation import ugettext_lazy as _

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = ROOT_DIR / "apps"
env = environ.Env()

# OS environment variables take precedence over variables from .env
# env.read_env(str(ROOT_DIR / ".env"))


# GENERAL
# -------------------------------------------------------------------

LANGUAGES = (
    ("en", _("English")),
    # ('de', _('German')),
)
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"
SITE_ID = env("DJANGO_SITE_ID", default=1)
USE_I18N = False
USE_L10N = True
USE_TZ = True
# LOCALE_PATHS = [str(ROOT_DIR / "locale")]


# DATABASES
# -------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", default=""),
        "NAME": env("SQL_DB", default=""),
        "USER": env("SQL_USER", default=""),
        "PASSWORD": env("SQL_PASSWORD", default=""),
        "HOST": env("SQL_HOST", default=""),
        "PORT": env("SQL_PORT", default=""),
    }
}

# URLS
# -------------------------------------------------------------------

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# -------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Handy template tags
    "django.contrib.flatpages",  # Contact
    "django.forms",
]

THIRD_PARTY_APPS = [
    "markdownify.apps.MarkdownifyConfig",
    "compressor",
    "django.contrib.admin",
    "adminsortable2",
]

LOCAL_APPS = [
    "apps.startpage",
    "apps.blog",
    "apps.projects",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIGRATIONS
# -------------------------------------------------------------------

# MIGRATION_MODULES = {"sites": "rattletat.contrib.sites.migrations"}

# AUTHENTICATION
# -------------------------------------------------------------------

# AUTHENTICATION_BACKENDS = [
#     "allauth.account.auth_backends.AuthenticationBackend",
# ]

# PASSWORDS
# -------------------------------------------------------------------

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# -------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Cache + Minify
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

# STATIC
# -------------------------------------------------------------------

STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/staticfiles/"
STATICFILES_DIRS = [str(ROOT_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",  # Minify
]

# MEDIA
# -------------------------------------------------------------------

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = ROOT_DIR / "mediafiles"

# TEMPLATES
# -------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ROOT_DIR / "templates")],
        "OPTIONS": {
            "libraries": {"active": "templatetags.active"},
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# -------------------------------------------------------------------

FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# -------------------------------------------------------------------

# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = "DENY"

# EMAIL
# -------------------------------------------------------------------

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend"
    # "DJANGO_EMAIL_BACKEND", default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_TIMEOUT = 5

# ADMIN
# -------------------------------------------------------------------

ADMIN_URL = "admin/"
ADMINS = []
MANAGERS = ADMINS

# LOGGING
# -------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# MARKDOWNIFY
# -------------------------------------------------------------------
from apps.blog.utils.markdown_prism import PrismCodeExtension
from markdown_checklist.extension import ChecklistExtension
from markdown_katex.extension import KatexExtension

MARKDOWNIFY = {
    "default": {
        "MARKDOWN_EXTENSIONS": [
            PrismCodeExtension(),
            ChecklistExtension(),
            KatexExtension(),
        ],
        "STRIP": False,
        "BLEACH": False,
    },
    "comment": {
        "WHITELIST_TAGS": [],
        "WHITELIST_ATTRS": [],
        "WHITELIST_STYLES": [],
        "WHITELIST_PROTOCOLS": [],
        "LINKIFY_TEXT": {
            "PARSE_URLS": True,
            "PARSE_EMAIL": True,
            "CALLBACKS": [],
            "SKIP_TAGS": [],
        },
    },
}
