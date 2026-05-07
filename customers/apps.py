from django.apps import AppConfig


class CustomersConfig(AppConfig):
    """Application configuration for the customers app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'