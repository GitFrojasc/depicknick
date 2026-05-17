from django.apps import AppConfig


class TiendaConfig(AppConfig):
    name = 'tienda'

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User

        def crear_perfil(sender, instance, created, **kwargs):
            if created:
                from .models import PerfilCliente
                from django.conf import settings
                from django.core.mail import send_mail
                PerfilCliente.objects.get_or_create(usuario=instance)
                send_mail(
                    subject=f'[Sumercá] Nuevo cliente: {instance.get_full_name() or instance.username}',
                    message=(
                        f'Se registró un nuevo cliente:\n\n'
                        f'Nombre: {instance.get_full_name() or instance.username}\n'
                        f'Email: {instance.email}\n'
                        f'Usuario: {instance.username}\n\n'
                        f'Verlo en el admin: /admin/auth/user/{instance.pk}/change/'
                    ),
                    from_email='Sumercá <onboarding@resend.dev>',
                    recipient_list=[settings.ADMIN_NOTIFY_EMAIL],
                    fail_silently=True,
                )

        post_save.connect(crear_perfil, sender=User)

