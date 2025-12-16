# Примеры использования API DjangoAuthAPI

Этот файл содержит практические примеры использования API с помощью `curl` и Python.

## 📋 Содержание

- [Аутентификация](#-аутентификация)
- [Управление пользователями](#-управление-пользователями)
- [RBAC система](#-rbac-система)
- [Mock объекты](#-mock-объекты)
- [Python примеры](#-python-примеры)

## 🔐 Аутентификация

### Регистрация нового пользователя

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Smith"
  }'
```

**Успешный ответ:**
```json
{
  "user": {
    "id": 3,
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Smith",
    "date_joined": "2025-12-16T00:00:00Z"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Логин пользователя

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepassword123"
  }'
```

**Успешный ответ:**
```json
{
  "user": {
    "id": 3,
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Smith",
    "date_joined": "2025-12-16T00:00:00Z"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Ошибка аутентификации

**Запрос с неверным паролем:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "wrongpassword"
  }'
```

**Ответ с ошибкой:**
```json
{
  "detail": "Неверные учетные данные"
}
```

### Обновление токена

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Успешный ответ:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Логаут

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Успешный ответ:**
```http
HTTP/1.1 205 Reset Content
```

## 👤 Управление пользователями

### Получение профиля пользователя

**Запрос:**
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Успешный ответ:**
```json
{
  "id": 3,
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "middle_name": "Smith",
  "date_joined": "2025-12-16T00:00:00Z"
}
```

### Обновление профиля

**Запрос:**
```bash
curl -X PATCH http://localhost:8000/api/users/profile/update/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnathan",
    "last_name": "Doe-Smith",
    "middle_name": "William"
  }'
```

**Успешный ответ:**
```json
{
  "id": 3,
  "email": "newuser@example.com",
  "first_name": "Johnathan",
  "last_name": "Doe-Smith",
  "middle_name": "William",
  "date_joined": "2025-12-16T00:00:00Z"
}
```

### Смена пароля

**Запрос:**
```bash
curl -X PATCH http://localhost:8000/api/users/profile/update/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "securepassword123",
    "new_password": "newsecurepassword456"
  }'
```

**Успешный ответ:**
```json
{
  "id": 3,
  "email": "newuser@example.com",
  "first_name": "Johnathan",
  "last_name": "Doe-Smith",
  "middle_name": "William",
  "date_joined": "2025-12-16T00:00:00Z"
}
```

### Удаление аккаунта

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/users/delete/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Успешный ответ:**
```json
{
  "message": "Аккаунт успешно удален"
}
```

## 🔐 RBAC Система

### Работа с ресурсами

**Создание ресурса:**
```bash
curl -X POST http://localhost:8000/api/rbac/resources/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый ресурс",
    "description": "Описание нового ресурса",
    "endpoint": "/api/new-resource/"
  }'
```

**Список ресурсов:**
```bash
curl -X GET http://localhost:8000/api/rbac/resources/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Работа с действиями

**Список действий:**
```bash
curl -X GET http://localhost:8000/api/rbac/actions/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Работа с разрешениями

**Создание разрешения:**
```bash
curl -X POST http://localhost:8000/api/rbac/permissions/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "resource": 1,
    "action": 1
  }'
```

### Работа с ролями

**Создание роли:**
```bash
curl -X POST http://localhost:8000/api/rbac/roles/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новая роль",
    "description": "Описание новой роли",
    "permissions": [1, 2, 3]
  }'
```

**Список ролей:**
```bash
curl -X GET http://localhost:8000/api/rbac/roles/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Назначение ролей пользователям

**Назначение роли пользователю:**
```bash
curl -X POST http://localhost:8000/api/rbac/user-roles/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user": 3,
    "role": 2
  }'
```

### Просмотр аудит логов

**Список аудит логов:**
```bash
curl -X GET http://localhost:8000/api/rbac/audit-logs/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📦 Mock Объекты

### Создание mock объекта

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/mock/objects/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тестовый объект",
    "description": "Описание тестового объекта для разработки"
  }'
```

**Успешный ответ:**
```json
{
  "id": 1,
  "name": "Тестовый объект",
  "description": "Описание тестового объекта для разработки",
  "created_at": "2025-12-16T00:00:00Z",
  "updated_at": "2025-12-16T00:00:00Z"
}
```

### Список mock объектов

**Запрос:**
```bash
curl -X GET http://localhost:8000/api/mock/objects/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Успешный ответ:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Тестовый объект",
      "description": "Описание тестового объекта для разработки",
      "created_at": "2025-12-16T00:00:00Z",
      "updated_at": "2025-12-16T00:00:00Z"
    }
  ]
}
```

### Обновление mock объекта

**Запрос:**
```bash
curl -X PUT http://localhost:8000/api/mock/objects/1/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Обновленный объект",
    "description": "Обновленное описание"
  }'
```

### Удаление mock объекта

**Запрос:**
```bash
curl -X DELETE http://localhost:8000/api/mock/objects/1/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 🐍 Python Примеры

### Аутентификация с Python

```python
import requests

# Регистрация
register_data = {
    "email": "pythonuser@example.com",
    "password": "pythonpassword123",
    "password_confirm": "pythonpassword123",
    "first_name": "Python",
    "last_name": "User"
}

response = requests.post("http://localhost:8000/api/auth/register/", json=register_data)
print("Register response:", response.json())

# Логин
login_data = {
    "email": "pythonuser@example.com",
    "password": "pythonpassword123"
}

response = requests.post("http://localhost:8000/api/auth/login/", json=login_data)
tokens = response.json()
access_token = tokens["access"]
print("Login successful, access token:", access_token)

# Использование токена
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get("http://localhost:8000/api/users/profile/", headers=headers)
print("Profile data:", response.json())
```

### Работа с RBAC

```python
import requests

# Предполагаем, что у нас есть access_token
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Создание ресурса
resource_data = {
    "name": "Python Resource",
    "description": "Resource created via Python",
    "endpoint": "/api/python-resource/"
}

response = requests.post("http://localhost:8000/api/rbac/resources/", 
                        json=resource_data, headers=headers)
print("Created resource:", response.json())

# Получение списка ресурсов
response = requests.get("http://localhost:8000/api/rbac/resources/", headers=headers)
print("Resources list:", response.json())

# Создание роли
role_data = {
    "name": "Python Role",
    "description": "Role created via Python",
    "permissions": []  # Можно добавить IDs разрешений
}

response = requests.post("http://localhost:8000/api/rbac/roles/", 
                        json=role_data, headers=headers)
print("Created role:", response.json())
```

### Работа с Mock объектами

```python
import requests

# Предполагаем, что у нас есть access_token
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Создание mock объекта
mock_data = {
    "name": "Python Mock Object",
    "description": "Mock object created via Python script"
}

response = requests.post("http://localhost:8000/api/mock/objects/", 
                        json=mock_data, headers=headers)
mock_object = response.json()
print("Created mock object:", mock_object)

# Обновление mock объекта
update_data = {
    "name": "Updated Python Mock Object",
    "description": "Updated description"
}

response = requests.put(f"http://localhost:8000/api/mock/objects/{mock_object['id']}/", 
                        json=update_data, headers=headers)
print("Updated mock object:", response.json())

# Удаление mock объекта
response = requests.delete(f"http://localhost:8000/api/mock/objects/{mock_object['id']}/", 
                           headers=headers)
print("Delete status:", response.status_code)
```

## 🔧 Обработка ошибок

### Типичные ошибки и их обработка

**Ошибка аутентификации (401):**
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer invalid_token"
```

**Ответ:**
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

**Ошибка доступа (403):**
```bash
curl -X POST http://localhost:8000/api/rbac/resources/ \
  -H "Authorization: Bearer user_token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test", "endpoint": "/test/"}'
```

**Ответ:**
```json
{
  "detail": "У вас недостаточно прав для выполнения этого действия."
}
```

**Ошибка валидации (400):**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid", "password": "short"}'
```

**Ответ:**
```json
{
  "email": ["Введите правильный адрес электронной почты."],
  "password": ["Обязательное поле.", "Убедитесь, что этот пароль содержит не менее 8 символов."]
}
```

## 📚 Полезные советы

1. **Храните токены безопасно**: Никогда не сохраняйте токены в коде или системе контроля версий
2. **Используйте HTTPS**: Всегда используйте HTTPS в продакшене для защиты токенов
3. **Обрабатывайте ошибки**: Всегда обрабатывайте ошибки в вашем клиентском коде
4. **Обновляйте токены**: Используйте refresh токены для получения новых access токенов
5. **Логируйте действия**: Используйте аудит логи для отслеживания важных действий

## 🎯 Заключение

Эти примеры покрывают основные сценарии использования API DjangoAuthAPI. Вы можете использовать их как основу для интеграции с вашим фронтендом или другими сервисами.

Для более подробной информации обратитесь к [документации Swagger](http://localhost:8000/swagger/) или исходному коду проекта.