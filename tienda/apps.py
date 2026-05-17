from django.apps import AppConfig


class TiendaConfig(AppConfig):
    name = 'tienda'

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User

        def crear_perfil(sender, instance, created, **kwargs):
            if created:
                from .models import PerfilCliente
                PerfilCliente.objects.get_or_create(usuario=instance)

        post_save.connect(crear_perfil, sender=User)
