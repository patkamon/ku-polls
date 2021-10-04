"""Apps."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """App config for poll app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
