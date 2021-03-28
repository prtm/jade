from .base import *

SECRET_KEY = env("DJANGO_SECRET_KEY")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)
}