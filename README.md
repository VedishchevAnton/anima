# Anima — Лендинг для продукции

Веб-приложение на Django 6 + Jinja2. Лендинг с формами обратной связи и калькулятором.

## Требования

- Python 3.14+
- Git

## Установка (без Docker)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/VedishchevAnton/anima.git
cd anima
```

### 2. Создать виртуальное окружение

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустить сервер

Для запуска без PostgreSQL (лендинг без БД):

```bash
set USE_SQLITE=1          # Windows
export USE_SQLITE=1       # Linux / macOS

python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000

### 5. (Опционально) Настройка PostgreSQL

Если нужна база данных, создайте файл `anima/local.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'anima',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Затем выполните миграции:

```bash
python manage.py migrate
```

---

## Запуск в Docker

### Что нужно установить

Установите **Docker Desktop**:
- Windows / macOS: https://www.docker.com/products/docker-desktop/
- Linux: https://docs.docker.com/engine/install/

### Запуск (одна команда)

```bash
git clone https://github.com/VedishchevAnton/anima.git
cd anima
docker compose up --build
```

Сайт будет доступен по адресу: http://localhost:8000

### Остановка

```bash
docker compose down
```

### Перезапуск (без пересборки)

```bash
docker compose up
```

---

## Структура проекта

```
anima/
├── anima/           # Настройки Django (settings, urls, wsgi)
├── landing/         # Приложение лендинга (views, templates)
├── static/          # Статические файлы (CSS, JS, изображения)
├── media/           # Загружаемые файлы
├── manage.py        # Точка входа Django
├── requirements.txt # Зависимости Python
├── Dockerfile       # Конфигурация Docker
└── docker-compose.yml
```
