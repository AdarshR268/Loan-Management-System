from django.apps import AppConfig

class LoansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loans'

    def ready(self):
        """Load signals, but don't start Celery tasks."""
        try:
            import loans.signals  # Load signals if they exist
        except ImportError:
            pass
