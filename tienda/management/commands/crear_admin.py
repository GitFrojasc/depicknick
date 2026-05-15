from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea o actualiza el superusuario de administración'

    def handle(self, *args, **options):
        username = 'francisco'
        email = 'francopacho79@gmail.com'
        password = 'depicknick2026'

        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" actualizado.'))
