#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'professional_writers.settings')
django.setup()

from writers_app.models import Service, ServicePackage

def create_sample_packages():
    services = Service.objects.all()
    
    for service in services:
        # Create Basic package
        basic_pkg, created = ServicePackage.objects.get_or_create(
            service=service,
            name='Basic',
            defaults={
                'description': 'Essential package for getting started',
                'price_inr': 2999,
                'price_usd': 39,
                'features': ['Professional formatting', 'ATS optimization', '2 revisions'],
                'delivery_days': 3,
                'revisions': 2,
                'display_order': 1
            }
        )
        if created:
            print(f'Created Basic package for {service.name}')
        
        # Create Premium package
        premium_pkg, created = ServicePackage.objects.get_or_create(
            service=service,
            name='Premium',
            defaults={
                'description': 'Most popular package with extra features',
                'price_inr': 4999,
                'price_usd': 69,
                'features': ['Professional formatting', 'ATS optimization', 'Cover letter', '5 revisions', 'LinkedIn optimization'],
                'delivery_days': 2,
                'revisions': 5,
                'is_popular': True,
                'display_order': 2
            }
        )
        if created:
            print(f'Created Premium package for {service.name}')
        
        # Create Professional package
        pro_pkg, created = ServicePackage.objects.get_or_create(
            service=service,
            name='Professional',
            defaults={
                'description': 'Complete package for serious professionals',
                'price_inr': 7999,
                'price_usd': 99,
                'features': ['Professional formatting', 'ATS optimization', 'Cover letter', 'LinkedIn optimization', 'Unlimited revisions', 'Rush delivery'],
                'delivery_days': 1,
                'revisions': 999,
                'display_order': 3
            }
        )
        if created:
            print(f'Created Professional package for {service.name}')

if __name__ == '__main__':
    create_sample_packages()
    print('Sample packages created successfully!')