# DjangoAuthAPI

**Современное API для аутентификации и управления доступом на Django**

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Описание проекта

DjangoAuthAPI - это готовое решение для аутентификации и управления доступом с использованием:

- **JWT аутентификация** (JSON Web Tokens)
- **RBAC система** (Role-Based Access Control)
- **Кастомная модель пользователя** с email аутентификацией
- **Полная документация API** через Swagger/OpenAPI
- **Аудит логирование** для отслеживания действий

## 🚀 Быстрый старт

### Использование Docker (рекомендуется)

#### Предварительные требования

- Docker
- Docker Compose

#### Установка и запуск

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/ваш-репозиторий/DjangoAuthAPI.git
cd DjangoAuthAPI
```

2. **Создайте файл `.env` в корне проекта:**

```env
# Основные настройки
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки базы данных (значения по умолчанию для Docker)
DB_NAME=django_auth_api
DB_USER=django_user
DB_PASSWORD=django_password
DB_HOST=db
DB_PORT=5432
```

3. **Запустите контейнеры с помощью Docker Compose:**

```bash
docker-compose up --build
```

4. **Выполните миграции:**

В новом терминале выполните:

```bash
docker-compose exec web python manage.py migrate
```

5. **Создайте суперпользователя:**

```bash
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Локальная установка (без Docker)

#### Предварительные требования

- Python 3.13+
- PostgreSQL
- pip

#### Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/ваш-репозиторий/DjangoAuthAPI.git
cd DjangoAuthAPI
```

2. **Создайте и активируйте виртуальное окружение:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения:**

Создайте файл `.env` в корне проекта:

```env
# Основные настройки
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки базы данных
DB_NAME=backend_db
DB_USER=backend_user
DB_PASSWORD=ваш-пароль
DB_HOST=localhost
DB_PORT=5432
```

5. **Выполните миграции:**

```bash
python manage.py migrate
```

6. **Создайте суперпользователя:**

```bash
python manage.py createsuperuser
```

7. **Запустите сервер разработки:**

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: `http://localhost:8000`

## 📖 Документация API

Документация API доступна через Swagger:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **OpenAPI JSON**: `http://localhost:8000/swagger.json/`

## 🔐 Аутентификация

### Регистрация

```bash
POST /api/auth/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Smith"
}
```

### Логин

```bash
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Ответ:**

```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "middle_name": "Smith",
        "date_joined": "2025-12-16T00:00:00Z"
    },
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Логаут

```bash
POST /api/auth/logout/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Обновление токена

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 👤 Управление пользователями

### Получение профиля

```bash
GET /api/users/profile/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Обновление профиля

```bash
PATCH /api/users/profile/update/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "first_name": "New Name",
    "last_name": "New Lastname",
    "middle_name": "New Middlename",
    "current_password": "oldpassword123",
    "new_password": "newpassword123"
}
```

### Удаление аккаунта

```bash
POST /api/users/delete/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 🔐 RBAC Система

### Ресурсы

- **Список ресурсов**: `GET /api/rbac/resources/`
- **Создание ресурса**: `POST /api/rbac/resources/`
- **Получение ресурса**: `GET /api/rbac/resources/{id}/`
- **Обновление ресурса**: `PUT /api/rbac/resources/{id}/`
- **Удаление ресурса**: `DELETE /api/rbac/resources/{id}/`

### Действия

- **Список действий**: `GET /api/rbac/actions/`
- **Создание действия**: `POST /api/rbac/actions/`
- **Получение действия**: `GET /api/rbac/actions/{id}/`
- **Обновление действия**: `PUT /api/rbac/actions/{id}/`
- **Удаление действия**: `DELETE /api/rbac/actions/{id}/`

### Разрешения

- **Список разрешений**: `GET /api/rbac/permissions/`
- **Создание разрешения**: `POST /api/rbac/permissions/`
- **Получение разрешения**: `GET /api/rbac/permissions/{id}/`
- **Обновление разрешения**: `PUT /api/rbac/permissions/{id}/`
- **Удаление разрешения**: `DELETE /api/rbac/permissions/{id}/`

### Роли

- **Список ролей**: `GET /api/rbac/roles/`
- **Создание роли**: `POST /api/rbac/roles/`
- **Получение роли**: `GET /api/rbac/roles/{id}/`
- **Обновление роли**: `PUT /api/rbac/roles/{id}/`
- **Удаление роли**: `DELETE /api/rbac/roles/{id}/`

### Связи пользователей с ролями

- **Список связей**: `GET /api/rbac/user-roles/`
- **Создание связи**: `POST /api/rbac/user-roles/`
- **Получение связи**: `GET /api/rbac/user-roles/{id}/`
- **Обновление связи**: `PUT /api/rbac/user-roles/{id}/`
- **Удаление связи**: `DELETE /api/rbac/user-roles/{id}/`

### Аудит логи

- **Список логов**: `GET /api/rbac/audit-logs/`
- **Получение лога**: `GET /api/rbac/audit-logs/{id}/`

## 📦 Mock Объекты

Для тестирования и разработки доступны mock объекты:

- **Список объектов**: `GET /api/mock/objects/`
- **Создание объекта**: `POST /api/mock/objects/`
- **Получение объекта**: `GET /api/mock/objects/{id}/`
- **Обновление объекта**: `PUT /api/mock/objects/{id}/`
- **Удаление объекта**: `DELETE /api/mock/objects/{id}/`

## 🛡️ Безопасность

### Аутентификация

- Все эндпоинты, кроме аутентификации, требуют JWT токен
- Токены имеют ограниченное время жизни
- Поддерживается обновление токенов

### Авторизация

- RBAC система управляет доступом к ресурсам
- Суперпользователи имеют полный доступ
- Обычные пользователи имеют доступ только к разрешенным ресурсам
- Все действия логируются в аудит логах

### Защита от атак

- CSRF защита включена
- CORS настроен для разрешенных доменов
- XSS защита через Django шаблоны
- SQL инъекции предотвращаются ORM

## 🔧 Настройка

### База данных

По умолчанию используется PostgreSQL. Вы можете изменить настройки в `.env` файле:

```env
DB_NAME=ваша_база_данных
DB_USER=ваш_пользователь
DB_PASSWORD=ваш_пароль
DB_HOST=ваш_хост
DB_PORT=ваш_порт
```

### JWT Настройки

Настройки JWT токенов можно изменить в `backend/settings.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

### CORS Настройки

Настройки CORS можно изменить в `backend/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## 🧪 Тестирование

### Создание тестовых пользователей

```bash
# Создать суперпользователя
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(email='admin@example.com', password='admin123', first_name='Admin', last_name='User')"

# Создать обычного пользователя
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user(email='user@example.com', password='user123', first_name='Regular', last_name='User')"
```

### Тестирование API

Вы можете использовать `curl` для тестирования API:

```bash
# Тестирование аутентификации
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Тестирование защищенных эндпоинтов
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer ВАШ_JWT_ТОКЕН"
```

## 📦 Зависимости

Основные зависимости проекта:

- Django 4.2.7
- Django REST Framework 3.14.0
- djangorestframework-simplejwt 5.3.0
- psycopg2-binary 2.9.9
- python-decouple 3.8
- django-cors-headers 4.3.1
- drf-yasg 1.21.7

## 🎯 Структура проекта

```
DjangoAuthAPI/
├── backend/                  # Основные настройки Django
│   ├── settings.py           # Конфигурация проекта
│   ├── urls.py               # Маршрутизация
│   └── ...
├── users/                    # Модуль пользователей
│   ├── models.py             # Модель пользователя
│   ├── serializers.py        # Сериализаторы
│   ├── views.py              # Представления
│   ├── urls.py               # Маршруты
│   └── ...
├── rbac/                     # RBAC система
│   ├── models.py             # Модели RBAC
│   ├── serializers.py        # Сериализаторы
│   ├── views.py              # Представления
│   ├── urls.py               # Маршруты
│   ├── permissions.py        # Кастомные разрешения
│   └── ...
├── mock_objects/             # Тестовые объекты
│   ├── models.py             # Модель mock объектов
│   ├── serializers.py        # Сериализаторы
│   ├── views.py              # Представления
│   └── urls.py               # Маршруты
├── manage.py                 # Управление Django
├── requirements.txt          # Зависимости
└── README.md                 # Документация
```
Для вопросов и поддержки:

- Email: support@djangoauthapi.com
- GitHub Issues: https://github.com/ваш-репозиторий/DjangoAuthAPI/issues

---
