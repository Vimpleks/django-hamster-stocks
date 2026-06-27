# Запасы Хомяка - Итоговый проект на курсе Python-разработчик

Приложение для учета ниток мулине.
Возможности приложения:
 
1. Справочник ниток мулине
2. Вести учет ниток, которые есть в запасе
3. Вести список ниток, которые необходимо купить.
4. Заносить данные о проектах для вышивания, необходимых нитках для проекта

#### Проект располагается в папке "app"

## Быстрый старт

### 1. Установить зависимости
```bash
poetry install
```

### 2. Создать базу данных PostgreSQL
```bash
createdb hamster_stocks
```

### 3. Применить миграции
```bash
poetry run python manage.py migrate
```

### 4. Создать суперпользователя
```bash
poetry run python manage.py createsuperuser
```

### 5. Загрузить фикстуры
```bash
poetry run python manage.py loaddata fixtures/threads/manufacturer.json
poetry run python manage.py loaddata fixtures/threads/thread.json
```

### 6. Запустить сервер
```bash
poetry run python manage.py runserver
```
Открыть: http://127.0.0.1:8000  
Admin: http://127.0.0.1:8000/admin

### 7. Запустить тесты
```bash
poetry run pytest -v
```