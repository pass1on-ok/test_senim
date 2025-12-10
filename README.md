# Senim Test Backend

Небольшой backend-проект на FastAPI с авторизацией по JWT и системой создания отчётов.

## Как запустить проект

### **Вариант 1 через Docker**

```bash
docker-compose up --build
После запуска сервис будет доступен здесь:
```

Наш сервис: http://localhost:8000/
Swagger UI: http://localhost:8000/docs

### **Вариант 2 вручную**

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите сервер:

```bash
uvicorn app.main:app --reload
```

## Как устроена аутентификация

Проект использует JWT-токены и механизм OAuth2PasswordBearer.
Основной процесс:
Пользоваетль регистрируется через `POST /auth/register`

Пользователь логинится через `POST /auth/login`

При успешной аутентификации сервер выдаёт JWT-токен.

Алгоритм:
 - Пользователь отправляет email + пароль
 - Сервер проверяет хэш пароля
 - Генерирует JWT и возвращает клиенту
 - Клиент использует токен для доступа к приватным ресурсам
 - Токен передаётся в заголовке каждого защищённого запроса:

`
Authorization: Bearer <token>
`
Текущий пользователь определяется через зависимость
get_current_user
`GET /auth/me`

Без токена доступ к защищённым маршрутам запрещён.

Правила доступа к `GET /reports`:

admin - видит все отчёты
staff - видит только свои

Примеры запросов отчета
Создание отчёта

`POST /reports`
```
{
  "category": "Bug",
  "message": "Found a critical bug in auth module"
}
```

Ответ:

```
{
  "id": 1,
  "category": "Bug",
  "message": "Found a critical bug in auth module",
  "created_at": "2025-12-10T21:45:00",
  "author": {
    "id": 2,
    "username": "staff1",
    "role": "staff"
  }
}
```
