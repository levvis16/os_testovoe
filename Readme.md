# Сервис для бронирования столика в ресторане

**Стек:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, SQLite

## Архитектура (слои)

- `app/routers` — HTTP-роуты (контроллеры), валидация входящих данных через Pydantic, делегирование в сервисы
- `app/schemas` — Pydantic-схемы запроса (`BookingCreate`) и ответа (`BookingOut`) с валидацией
- `app/services` — бизнес-логика: создание, чтение, отмена броней, проверка уникальности слота
- `app/models` — SQLAlchemy-модели, таблица `bookings` с уникальным частичным индексом на `(booking_date, booking_time)` где `status='active'`
- `app/database` — подключение к SQLite, сессии, миграции через `Base.metadata.create_all`

## Запуск

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить сервер
uvicorn main:app --reload
```

Сервер поднимется на `http://127.0.0.1:8000`

## Документация API (Swagger UI)

Открыть в браузере: **http://127.0.0.1:8000/docs**

## Эндпоинты

| POST | `/bookings` | Создать бронь. Возвращает 201 и бронь со `status=active` |
| GET | `/bookings` | Список броней. Фильтр по дате: `?date=2026-12-15` |
| GET | `/bookings/{id}` | Получить бронь по ID. 404 если не найдена |
| DELETE | `/bookings/{id}` | Отменить бронь: статус → `cancelled`. Возвращает 200 и бронь |

## Правила валидации (Pydantic)

- `name`: 2–50 символов
- `phone`: формат `+7XXXXXXXXXX` (ровно 10 цифр после +7)
- `booking_date`: не в прошлом, не дальше 30 дней от сегодня
- `booking_time`: только целые часы с 12:00 до 22:00
- `guests`: 1–10

## Главное бизнес-правило

**На одну дату и время может быть только одна активная бронь.**  
Повторная попытка → `409 Conflict` с `{"detail": "Slot is already booked"}`.  
Отменённая бронь (`status=cancelled`) слот **не занимает** — можно заново забронировать то же время.

## Тесты

```bash
# Запуск всех тестов
pytest app/tests/ -v
```


## Что доделал бы при наличии времени

1. **Аутентификация/авторизация** (JWT, роли: клиент/админ) — сейчас API открыто.
2. **PostgreSQL в проде** — миграции через Alembic, connection pooling, частичные индексы нативно.
3. **Логирование** (structlog) и метрики (Prometheus) — observability.
4. **Интеграционные тесты** с Testcontainers (PostgreSQL) + CI/CD (GitHub Actions).
5. **Dockerfile** и `docker-compose.yml` для локального запуска одной командой.
