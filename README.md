# Flask User Management API

Простий REST API для керування користувачами, розроблений з використанням Flask, SQLAlchemy та PostgreSQL.

## Технології

- Python 3.12
- Flask
- SQLAlchemy
- PostgreSQL
- Docker
- pytest

## Структура проєкту

```shell
test-task-gyb-flask-api/
├── app/
# Ініціалізація додатку
│   ├── __init__.py
# Налаштування бази даних     
│   ├── database.py
# Моделі даних
│   ├── models.py
# API ендпоінти
│   ├── routes.py
# Схеми валідації
│   └── schemas.py 
# Тести       
├── tests/
# Налаштування Docker                
├── Dockerfile  
# Налаштування Docker Compose          
├── docker-compose.yml
# Точка входу    
└── main.py               
```



# Встановлення та запуск

Найпростіший спосіб запустити проект - використовувати Docker Compose:

## Через Docker

```bash
# Клонуйте репозиторій
git clone https://github.com/Le0n-K/test-task-gyb-flask-api/pull/1

cd test-task-gyb-flask-api

# Запустіть контейнери
docker-compose up --build
```

API буде доступне за адресою: [http://localhost:5000](http://localhost:5000)

Документація Swagger буде доступна за адресою: [http://localhost:5000/swagger/](http://localhost:5000/swagger/)


## Локально
Для локального встановлення вам потрібен Python 3.12 та PostgreSQL:

```bash
# Клонуйте репозиторій
git clone https://github.com/Le0n-K/test-task-gyb-flask-api/pull/1

cd test-task-gyb-flask-api
```

### Створіть віртуальне середовище
```bash
python -m venv venv
# На Mac:
source venv/bin/activate  
# На Windows: 
venv\Scripts\activate
```

### Встановіть залежності
```bash
pip install poetry
poetry install
```

### Створіть базу даних PostgreSQL
```bash
createdb users_db
```
### Налаштуйте змінні середовища:
```bash
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/users_db"
```

### Запустіть додаток
```bash
python main.py
```

API буде доступне за адресою: [http://localhost:5000](http://localhost:5000)

Документація Swagger буде доступна за адресою: [http://localhost:5000/swagger/](http://localhost:5000/swagger/)

## API Ендпоінти

| Метод  | URL         | Опис                                  |
|--------|-------------|---------------------------------------|
| GET    | /users      | Отримання списку всіх користувачів    |
| POST   | /users      | Створення нового користувача          |
| GET    | /users/:id  | Отримання інформації про користувача  |
| PUT    | /users/:id  | Оновлення даних користувача           |
| DELETE | /users/:id  | Видалення користувача                 |


## Приклади запитів

### Отримання всіх користувачів
```bash
curl -X GET http://localhost:5000/users
```

### Отримання конкретного користувача
```bash
curl -X GET http://localhost:5000/users/1
```

### Оновлення користувача
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated", "email": "john.updated@example.com"}'
```

### Видалення користувача
```bash
curl -X DELETE http://localhost:5000/users/1
```

## Модель користувача

- id: цілочисельний, первинний ключ
- name: рядок
- email: рядок, унікальний
- created_at: дата/час створення

## Тестування
Проект включає комплексні тести, які перевіряють всі ендпоінти API та обробку помилок.

### Запуск тестів
```bash
# Локально
pytest

# В Docker
docker-compose exec web pytest
```