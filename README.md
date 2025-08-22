# Менеджер Задча==ач

Простое API для управления задачами на **FastAPI**.  
Реализован полный CRUD: создание, просмотр, обновление и удаление задач.  
Проект включает тесты на **pytest** и миграции через **Alembic**.

---

## Стек технологий
- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- SQLite (по умолчанию)
- Pytest

---

## Установка и запуск

Клонируем проект:
```bash
git clone https://github.com/username/task_manager.git
cd task_manager
```

Создаём и активируем виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```
Устанавливаем зависимости
```bash
pip install -r requirements.txt
```

Применяем миграции:
```bash
alembic upgrade head
```

Запускаем сервер:
```bash
uvicorn app.main:app --reload
```

## Документация API

После запуска доступна по адресу:
http://127.0.0.1:8000/docs


