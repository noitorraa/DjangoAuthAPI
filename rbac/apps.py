from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rbac"

    def ready(self):
        # Инициализация RBAC при запуске приложения
        try:
            from .utils import initialize_rbac

            initialize_rbac()
        except Exception as e:
            print(f"Ошибка при инициализации RBAC: {e}")
