#!/usr/bin/env python
# Archivo regenerado correctamente
"""
WSGI config for the project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Para que Vercel lo detecte fácilmente en serverless:
app = application
