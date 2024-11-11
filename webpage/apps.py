"""Import the essential package for AppConfig."""
from django.apps import AppConfig


class WebpageConfig(AppConfig):
    """App config for the web app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webpage'

    def ready(self):
        """Import signals after making change in the admin page."""
        import webpage.signals
