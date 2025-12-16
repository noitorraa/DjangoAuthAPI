from .models import Resource, Action, Permission, Role


def initialize_rbac():
    """Инициализация базовых данных RBAC"""

    # Создаем действия
    actions_data = [
        {"name": "Просмотр", "code": "view", "description": "Просмотр ресурса"},
        {
            "name": "Создание",
            "code": "create",
            "description": "Создание нового ресурса",
        },
        {
            "name": "Редактирование",
            "code": "edit",
            "description": "Редактирование ресурса",
        },
        {"name": "Удаление", "code": "delete", "description": "Удаление ресурса"},
    ]

    for action_data in actions_data:
        Action.objects.get_or_create(**action_data)

    # Создаем ресурсы для пользователей
    user_resources = [
        {
            "name": "Пользователи",
            "endpoint": "/api/users/",
            "description": "Управление пользователями",
        },
        {
            "name": "Профиль",
            "endpoint": "/api/users/profile/",
            "description": "Профиль пользователя",
        },
        {
            "name": "Аутентификация",
            "endpoint": "/api/auth/",
            "description": "Аутентификация и регистрация",
        },
    ]

    for resource_data in user_resources:
        Resource.objects.get_or_create(**resource_data)

    # Создаем базовые роли
    roles_data = [
        {
            "name": "Администратор",
            "description": "Полный доступ ко всем функциям",
            "is_default": False,
        },
        {"name": "Пользователь", "description": "Базовый доступ", "is_default": True},
        {
            "name": "Менеджер",
            "description": "Доступ к управлению контентом",
            "is_default": False,
        },
    ]

    for role_data in roles_data:
        Role.objects.get_or_create(**role_data)

    # Даем администратору все разрешения
    admin_role = Role.objects.get(name="Администратор")
    for resource in Resource.objects.all():
        for action in Action.objects.all():
            permission, _ = Permission.objects.get_or_create(
                resource=resource, action=action
            )
            admin_role.permissions.add(permission)

    print("RBAC система инициализирована")
