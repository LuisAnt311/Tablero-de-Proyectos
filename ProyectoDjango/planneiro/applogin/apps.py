from django.apps import AppConfig


class ApploginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applogin'
    def ready(self):
            import applogin.signals  # Importa las señales aquí