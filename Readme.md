# Сервис для бронирования столика в ресторане

Python 3.13, FastAPI.

Слои:

- `app/routers` — HTTP-роуты
- `app/schemas` — pydantic-схемы запроса и ответа
- `app/services` — правила бронирования
- `app/models` — таблица в базе
- `app/database` — подключение к SQLite

Запуск:

```
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Документация: http://127.0.0.1:8000/docs
