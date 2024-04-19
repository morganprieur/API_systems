from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard' 

    def ready(self):

        # Implicitly connect signal handlers decorated with @receiver. 
        from . import signals 

