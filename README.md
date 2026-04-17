# Anima — Лендинг для кофейного оборудования

Веб-приложение на FastAPI + Jinja2.

## Требования

- Python 3.10+
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

```bash
uvicorn main:app --reload
```

Сайт будет доступен по адресу: http://127.0.0.1:8000

### 5. Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DEBUG` | `true` — заявки выводятся в консоль, `false` — отправляются на почту | `false` |
| `EMAIL_HOST` | SMTP-сервер (например `smtp.mail.ru`) | — |
| `EMAIL_PORT` | Порт SMTP | `465` |
| `EMAIL_USER` | Логин SMTP (e-mail отправителя) | — |
| `EMAIL_PASSWORD` | Пароль приложения (не пароль от почты!) | — |
| `EMAIL_FROM` | Адрес отправителя | `anima.market@mail.ru` |
| `FEEDBACK_EMAIL` | Куда приходят заявки | `anima.market@mail.ru` |
| `RECAPTCHA_SITE_KEY` | Ключ сайта reCAPTCHA v2 | тестовый ключ |
| `RECAPTCHA_SECRET_KEY` | Секретный ключ reCAPTCHA v2 | тестовый ключ |

> **Тестовые ключи reCAPTCHA** работают на любом домене (включая localhost).
> Для продакшена замените их на свои ключи из [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin).

### Настройка для продакшена

Задайте переменные окружения перед запуском:

**Linux / macOS:**
```bash
export DEBUG=false
export EMAIL_HOST=smtp.mail.ru
export EMAIL_USER=anima.market@mail.ru
export EMAIL_PASSWORD=пароль_приложения
export RECAPTCHA_SITE_KEY=ваш_ключ_сайта
export RECAPTCHA_SECRET_KEY=ваш_секретный_ключ
```

**Windows (PowerShell):**
```powershell
$env:DEBUG="false"
$env:EMAIL_HOST="smtp.mail.ru"
$env:EMAIL_USER="anima.market@mail.ru"
$env:EMAIL_PASSWORD="пароль_приложения"
$env:RECAPTCHA_SITE_KEY="ваш_ключ_сайта"
$env:RECAPTCHA_SECRET_KEY="ваш_секретный_ключ"
```

### Для локальной разработки

Если хотите тестировать отправку формы без почты, задайте `DEBUG=true`:
```powershell
$env:DEBUG="true"
uvicorn main:app --reload
```
Заявки будут выводиться в консоль.

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

---

## Структура проекта

```
anima/
├── main.py              # FastAPI приложение
├── config.py            # Настройки (env-переменные)
├── data.py              # Данные для шаблонов
├── templates/           # Jinja2 шаблоны
├── static/              # CSS, JS, изображения, шрифты
├── requirements.txt     # Зависимости Python
├── Dockerfile
└── docker-compose.yml
```
