from .base import *

SECRET_KEY = env("DJANGO_SECRET_KEY")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)
}

# STATIC
# ------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


CORS_ALLOWED_ORIGINS = [
    "https://awesome-jade.netlify.app",
]