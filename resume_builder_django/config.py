import os

# Used by settings.py
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-temp-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
