import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cafe.com', 'admin123')
    print('✓ Superuser "admin" created successfully')
    print('  Username: admin')
    print('  Password: admin123')
else:
    print('✓ Superuser already exists')
