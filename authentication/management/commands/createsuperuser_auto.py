"""
Django management command to create a superuser automatically.
This is useful for deployment environments where shell access isn't available.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create a superuser automatically using environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Admin username (or set DJANGO_SUPERUSER_USERNAME env var)',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Admin email (or set DJANGO_SUPERUSER_EMAIL env var)',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin password (or set DJANGO_SUPERUSER_PASSWORD env var)',
        )

    def handle(self, *args, **options):
        # Get credentials from arguments or environment variables
        username = (
            options['username'] or 
            os.environ.get('DJANGO_SUPERUSER_USERNAME') or 
            'admin'
        )
        email = (
            options['email'] or 
            os.environ.get('DJANGO_SUPERUSER_EMAIL') or 
            'admin@movierecommendations.com'
        )
        password = (
            options['password'] or 
            os.environ.get('DJANGO_SUPERUSER_PASSWORD') or 
            'admin123456'
        )

        try:
            # Check if superuser already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists. Skipping creation.')
                )
                return

            # Create superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
            
            # Don't print password in logs for security
            if os.environ.get('DJANGO_SUPERUSER_PASSWORD'):
                self.stdout.write(
                    self.style.SUCCESS('Password: [from environment variable]')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Password: admin123456 (CHANGE THIS IMMEDIATELY!)')
                )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )