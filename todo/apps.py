from django.apps import AppConfig
from django.db.models.signals import post_migrate

class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'
    def ready(self):
        from . import signals