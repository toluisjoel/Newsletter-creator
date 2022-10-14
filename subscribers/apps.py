from django.apps import AppConfig


class SubscribersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscribers'
    
    def ready(self) -> None:
        from . import signals
