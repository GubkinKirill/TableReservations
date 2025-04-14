# Table Reservations API

API-сервис для управления столиками и бронированиями в ресторане.

## Описание

Этот сервис позволяет:
- управлять столиками (создание, удаление, просмотр)
- создавать и просматривать бронирования
- проверять наличие конфликтов при бронировании

Технологии:
- **FastAPI** — фреймворк для API
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Docker + docker-compose** — контейнеризация
- **Pytest** — тестирование

## Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/GubkinKirill/TableReservations.git
cd TableReservations
```

### 2. Запуск с Docker
```bash
docker-compose up --build
```

### 3. Открыть Swagger UI
[http://localhost:8000/docs](http://localhost:8000/docs)

## Тестирование
```bash
docker-compose exec web pytest
```

## Структура проекта

```
app/
├── models/          # SQLAlchemy модели
├── routers/         # FastAPI маршруты
├── schemas/         # Pydantic-схемы
├── services/        # Бизнес-логика
├── database.py      # Подключение к БД
├── main.py          # Точка входа
alembic/             # Миграции Alembic
tests/               # Тесты Pytest
```

## Alembic

Создать миграцию:
```bash
docker-compose exec web alembic revision --autogenerate -m "init"
```

Применить миграции:
```bash
docker-compose exec web alembic upgrade head
```

## .env файл

Создайте `.env` файл в корне проекта на основе `.env.example`:

```bash
cp .env.example .env


