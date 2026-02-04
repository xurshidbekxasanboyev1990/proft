"""
Django management command to create initial roles and permissions.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup initial data for the portfolio system'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-demo-users',
            action='store_true',
            help='Create demo users for testing',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        if options['create_demo_users']:
            self.create_demo_users()
        
        self.stdout.write(self.style.SUCCESS('Initial setup completed!'))
    
    def create_demo_users(self):
        """Create demo users for each role."""
        
        demo_users = [
            {
                'username': 'superadmin',
                'email': 'superadmin@example.com',
                'password': 'SuperAdmin123!',
                'role': 'superadmin',
                'first_name': 'Super',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'Admin123!',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
            },
            {
                'username': 'teacher1',
                'email': 'teacher1@example.com',
                'password': 'Teacher123!',
                'role': 'teacher',
                'first_name': 'John',
                'last_name': 'Teacher',
                'department': 'Computer Science',
                'position': 'Senior Lecturer',
            },
            {
                'username': 'teacher2',
                'email': 'teacher2@example.com',
                'password': 'Teacher123!',
                'role': 'teacher',
                'first_name': 'Jane',
                'last_name': 'Educator',
                'department': 'Mathematics',
                'position': 'Associate Professor',
            },
        ]
        
        for user_data in demo_users:
            password = user_data.pop('password')
            username = user_data['username']
            
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'User {username} already exists, skipping...')
                continue
            
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {username} (role: {user.role})')
            )
        
        self.stdout.write(self.style.SUCCESS('\nDemo users created!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  - superadmin / SuperAdmin123!')
        self.stdout.write('  - admin / Admin123!')
        self.stdout.write('  - teacher1 / Teacher123!')
        self.stdout.write('  - teacher2 / Teacher123!')
