from .base import *  # noqa
from .base import env

# GENERAL
# -------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="unsecure-dev-key"
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# -------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# -------------------------------------------------------------------

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = "posteo.de"
EMAIL_HOST_USER = "michael.brauweiler@posteo.net"
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_PASSWORD", default="")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# WhiteNoise
# -------------------------------------------------------------------

INSTALLED_APPS = INSTALLED_APPS  # noqa F405

# django-debug-toolbar
# -------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
