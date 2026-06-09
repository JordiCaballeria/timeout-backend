import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TimeOut.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

User.objects.filter(username='admin').delete()
User.objects.create_superuser(
    username='admin',
    email='admin@admin.com',
    password='admin',
    first_name='Admin',
    last_name='Admin',
    is_active=True,
)
print('Superusuari creat correctament')
