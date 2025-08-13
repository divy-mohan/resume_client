#!/usr/bin/env python
"""
Django Development Server Runner

Simple script to run the Django development server.
Use this for local development.
"""

import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'professional_writers.settings')
    django.setup()
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5000'])