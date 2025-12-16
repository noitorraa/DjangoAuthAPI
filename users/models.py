from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей для email аутентификации
    
    Основные функции:
    - create_user: Создание обычного пользователя
    - create_superuser: Создание суперпользователя (администратора)
    
    Особенности:
    - Использует email вместо username для аутентификации
    - Валидация обязательных полей
    - Нормализация email адресов
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создание обычного пользователя
        
        Args:
            email (str): Email пользователя (используется как username)
            password (str): Пароль пользователя
            **extra_fields: Дополнительные поля (first_name, last_name, etc.)
            
        Returns:
            CustomUser: Созданный пользователь
            
        Raises:
            ValueError: Если email не указан
        """
        if not email:
            raise ValueError(_("Email обязателен"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создание суперпользователя (администратора)
        
        Args:
            email (str): Email администратора
            password (str): Пароль администратора
            **extra_fields: Дополнительные поля
            
        Returns:
            CustomUser: Созданный суперпользователь
            
        Raises:
            ValueError: Если не установлены необходимые флаги
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    
    Основные изменения от стандартной модели:
    - Удалено поле username (используется email)
    - Добавлено поле middle_name для отчества
    - Добавлено поле deleted_at для мягкого удаления
    - Email используется как уникальный идентификатор
    
    Поля:
    - email: Уникальный email (используется для аутентификации)
    - first_name: Имя (обязательное)
    - last_name: Фамилия (обязательное)
    - middle_name: Отчество (необязательное)
    - deleted_at: Дата мягкого удаления
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    middle_name = models.CharField(
        _("middle name"), max_length=50, blank=True, null=True
    )
    deleted_at = models.DateTimeField(_("deleted at"), blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def soft_delete(self):
        """
        Мягкое удаление пользователя
        
        Вместо физического удаления:
        - Деактивирует аккаунт (is_active = False)
        - Устанавливает дату удаления
        - Сохраняет пользователя в базе
        
        Это позволяет восстановить аккаунт при необходимости
        """
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
