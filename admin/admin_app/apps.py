from django.apps import AppConfig


class AdminAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_app"
    verbose_name = "Usuarios externos"

    def ready(self):
        from admin_app import signals  # noqa: F401
