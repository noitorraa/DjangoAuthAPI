from rest_framework import permissions
from django.urls import resolve
from .models import Resource, Action, Permission, UserRole


class HasPermission(permissions.BasePermission):
    """Проверка прав доступа пользователя"""

    def has_permission(self, request, view) -> bool:
        # Разрешаем доступ к Swagger без авторизации
        if request.path.startswith("/swagger/") or request.path.startswith("/redoc/"):
            return True

        # Проверяем аутентификацию
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем активность пользователя
        if not request.user.is_active:
            return False

        # Суперпользователь имеет все права
        if request.user.is_superuser:
            return True

        # Получаем текущий эндпоинт
        try:
            resolved = resolve(request.path_info)
            endpoint = f"{resolved.route}"
        except Exception:
            endpoint = request.path

        # Определяем действие на основе HTTP метода
        method_actions = {
            "GET": "view",
            "POST": "create",
            "PUT": "edit",
            "PATCH": "edit",
            "DELETE": "delete",
        }
        action_code = method_actions.get(request.method, "view")

        # Ищем разрешение
        try:
            resource = Resource.objects.get(endpoint__icontains=endpoint)
            action = Action.objects.get(code=action_code)
            permission = Permission.objects.get(resource=resource, action=action)

            # Проверяем, есть ли у пользователя роль с таким разрешением
            user_roles = UserRole.objects.filter(user=request.user)
            for user_role in user_roles:
                if permission in user_role.role.permissions.all():
                    return True

        except (Resource.DoesNotExist, Action.DoesNotExist, Permission.DoesNotExist):
            # Если для эндпоинта не настроены права - разрешаем доступ
            return True

        return False
