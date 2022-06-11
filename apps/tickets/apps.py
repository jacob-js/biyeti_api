from django.apps import AppConfig


class TicketsConfig(AppConfig): # pylint: disable=C0115
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tickets'
