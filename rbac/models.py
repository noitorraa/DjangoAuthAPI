from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Resource(models.Model):
    """
    Ресурсы системы
    
    Представляют защищаемые сущности в системе, к которым применяются разрешения.
    
    Поля:
    - name: Уникальное название ресурса
    - description: Описание ресурса
    - endpoint: URL путь для идентификации ресурса
    - created_at: Дата создания
    
    Примеры ресурсов:
    - Пользователи (/api/users/)
    - Профили (/api/users/profile/)
    - Аутентификация (/api/auth/)
    """

    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)
    endpoint = models.CharField(_("endpoint"), max_length=200, unique=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("resource")
        verbose_name_plural = _("resources")

    def __str__(self) -> str:
        return self.name


class Action(models.Model):
    """
    Действия над ресурсами
    
    Определяют типы операций, которые можно выполнять над ресурсами.
    
    Поля:
    - name: Название действия (например, "Просмотр")
    - code: Код действия для программной идентификации (например, "view")
    - description: Описание действия
    
    Стандартные действия:
    - view: Просмотр
    - create: Создание
    - edit: Редактирование
    - delete: Удаление
    """

    name = models.CharField(_("name"), max_length=50, unique=True)
    code = models.CharField(_("code"), max_length=50, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("action")
        verbose_name_plural = _("actions")

    def __str__(self) -> str:
        return self.name


class Permission(models.Model):
    """
    Разрешение = Ресурс + Действие
    
    Определяет конкретное разрешение для выполнения действия над ресурсом.
    
    Поля:
    - resource: Ресурс, к которому применяется разрешение
    - action: Действие, которое разрешено
    - created_at: Дата создания разрешения
    
    Примеры разрешений:
    - "Просмотр Пользователей"
    - "Редактирование Профиля"
    - "Удаление Аутентификации"
    """

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="permissions"
    )
    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, related_name="permissions"
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")
        unique_together = ["resource", "action"]

    def __str__(self) -> str:
        return f"{self.action.name} {self.resource.name}"


class Role(models.Model):
    """
    Роли пользователей
    
    Группируют наборы разрешений для удобного управления доступом.
    
    Поля:
    - name: Уникальное название роли
    - description: Описание роли
    - permissions: Набор разрешений, связанных с ролью
    - is_default: Флаг, указывающий на роль по умолчанию для новых пользователей
    - created_at: Дата создания роли
    
    Стандартные роли:
    - Администратор: Полный доступ ко всем функциям
    - Пользователь: Базовый доступ
    - Менеджер: Доступ к управлению контентом
    """

    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True)
    is_default = models.BooleanField(_("is default"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self) -> str:
        return self.name


class UserRole(models.Model):
    """
    Связь пользователей с ролями
    
    Определяет, какие роли назначены конкретным пользователям.
    
    Поля:
    - user: Пользователь, которому назначена роль
    - role: Роль, назначенная пользователю
    - created_at: Дата назначения роли
    
    Особенности:
    - Один пользователь может иметь несколько ролей
    - Одна роль может быть назначена нескольким пользователям
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("user role")
        verbose_name_plural = _("user roles")
        unique_together = ["user", "role"]

    def __str__(self) -> str:
        return f"{self.user.email} - {self.role.name}"


class AuditLog(models.Model):
    """
    Логирование действий администратора
    
    Отслеживает все важные действия в системе для аудита и безопасности.
    
    Поля:
    - user: Пользователь, выполнивший действие (может быть NULL для системных действий)
    - action: Тип действия (create, update, delete, etc.)
    - resource: Ресурс, над которым выполнено действие
    - details: Подробная информация о действии в JSON формате
    - ip_address: IP адрес пользователя
    - user_agent: Информация о браузере/клиенте
    - created_at: Дата и время действия
    
    Использование:
    - Отслеживание изменений в системе
    - Анализ безопасности
    - Восстановление данных
    """

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="audit_logs"
    )
    action = models.CharField(_("action"), max_length=200)
    resource = models.CharField(_("resource"), max_length=200)
    details = models.JSONField(_("details"), default=dict)
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("audit log")
        verbose_name_plural = _("audit logs")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.email if self.user else 'System'} - {self.action}"
