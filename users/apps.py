from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


def _create_digitador_group():
    from django.contrib.auth.models import Group

    Group.objects.get_or_create(name="Digitador")


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        try:
            _create_digitador_group()
        except (OperationalError, ProgrammingError):
            pass  # BD aún no lista (primera migración)
