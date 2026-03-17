# Habit Tracker (Atomic Habits)

Бэкенд-часть SPA веб-приложения для трекинга привычек, основанного на книге Джеймса Клира "Атомные привычки".

## Возможности

- Регистрация и авторизация пользователей
- CRUD для привычек с валидацией по правилам книги
- Публичные привычки (доступны всем)
- Интеграция с Telegram для напоминаний
- Отложенные задачи через Celery
- Пагинация (5 привычек на страницу)
- Документация API (Swagger/ReDoc)

## Технологии

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis (брокер Celery)
- Celery
- Telegram Bot API

## Установка и запуск

### Локальный запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker