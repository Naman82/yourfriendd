# images/management/commands/createsu.py

# from django.contrib.auth.models import User
from authentication.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@mail.com').exists():
            User.objects.create_superuser(
                # username='admin',
                email='admin@mail.com',
                password='Naman@2002'
            )
        print('Superuser has been created.')