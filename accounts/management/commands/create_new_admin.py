from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a new admin user from environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(self.style.ERROR('DJANGO_SUPERUSER_PASSWORD environment variable is required'))
            return
            
        # Check if user exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)  # Reset password
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user {username} updated with new password'))
        else:
            # Create new superuser
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Admin user {username} created successfully')) 