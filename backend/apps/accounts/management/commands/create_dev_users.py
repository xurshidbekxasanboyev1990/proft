"""
Management command to create development users for testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create development users for testing frontend-backend integration'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'superadmin',
                'email': 'superadmin@example.com',
                'password': 'superadmin123',
                'role': 'superadmin',
                'first_name': 'Super',
                'last_name': 'Admin',
                'department': 'IT Bo\'limi',
                'position': 'Tizim administratori',
            },
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'department': 'Pedagogika',
                'position': 'Fakultet dekani',
            },
            {
                'username': 'teacher',
                'email': 'teacher@example.com',
                'password': 'teacher123',
                'role': 'teacher',
                'first_name': 'Aliyev',
                'last_name': 'Vali',
                'department': 'Pedagogika',
                'position': 'Katta o\'qituvchi',
            },
            {
                'username': 'teacher2',
                'email': 'teacher2@example.com',
                'password': 'teacher123',
                'role': 'teacher',
                'first_name': 'Karimova',
                'last_name': 'Nilufar',
                'department': 'IT',
                'position': 'Dotsent',
            },
        ]

        for user_data in users_data:
            username = user_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists, skipping...')
                )
                continue

            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Created user: {username} ({user_data.get("role")})')
            )

        self.stdout.write(self.style.SUCCESS('\nDevelopment users created successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  superadmin / superadmin123 (Full access)')
        self.stdout.write('  admin / admin123 (Admin access)')
        self.stdout.write('  teacher / teacher123 (Teacher access)')
        self.stdout.write('  teacher2 / teacher123 (Teacher access)')
