#!/usr/bin/env python
"""
Django WSGI Application Entry Point

This file serves as the WSGI application entry point for the Professional Writers Django application.
It can be used with gunicorn or other WSGI servers.
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'professional_writers.settings')
django.setup()

# WSGI application
app = get_wsgi_application()

if __name__ == '__main__':
    """Run Django development server for testing"""
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5000'])