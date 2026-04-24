import smtplib
from email.mime.text import MIMEText

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from data import (
    CONTACT_INFO,
    NAV_ITEMS,
    RENT_FEATURES,
    RENT_ITEMS,
    ROASTING_FEATURES,
    SELECTION_CARDS,
    SOCIAL_LINKS,
)

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=500)


class CacheStaticMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=2592000"
        return response


app.add_middleware(CacheStaticMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


_cached_html: str | None = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global _cached_html
    if _cached_html is None:
        response = templates.TemplateResponse(
            request,
            "index.html",
            {
                "page_title": "Anima — техника для кофе в Екатеринбурге",
                "page_description": "Обслуживание, ремонт, подбор, аренда кофейного оборудования",
                "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
                "YANDEX_MAP_API_KEY": settings.YANDEX_MAP_API_KEY,
                "nav_items": NAV_ITEMS,
                "social_links": SOCIAL_LINKS,
                "rent_features": RENT_FEATURES,
                "roasting_features": ROASTING_FEATURES,
                "selection_cards": SELECTION_CARDS,
                "contact_info": CONTACT_INFO,
                "rent_items": RENT_ITEMS,
            },
        )
        _cached_html = response.body.decode()
    return HTMLResponse(_cached_html)


async def check_recaptcha(token: str) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": token,
            },
        )
        return resp.json().get("success", False)


def send_email(subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = settings.FEEDBACK_EMAIL

    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10) as server:
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.send_message(msg)


@app.post("/feedback/")
async def feedback(
    first_name: str = Form(""),
    last_name: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    message: str = Form(""),
    g_recaptcha_response: str = Form("", alias="g-recaptcha-response"),
):
    if not g_recaptcha_response or not await check_recaptcha(g_recaptcha_response):
        return JSONResponse({"status": False, "error_captcha": "Подтвердите, что вы не робот"})

    first_name = first_name.strip()
    last_name = last_name.strip()
    phone = phone.strip()
    email = email.strip()
    message = message.strip()

    errors = {}
    if not first_name:
        errors["first_name"] = "Введите имя"
    if not last_name:
        errors["last_name"] = "Введите фамилию"
    if not phone or len("".join(c for c in phone if c.isdigit())) < 11:
        errors["phone"] = "Введите корректный номер телефона"
    if not email or "@" not in email:
        errors["email"] = "Введите корректный e-mail"
    if not message:
        errors["message"] = "Введите сообщение"

    if errors:
        return JSONResponse({"status": False, "errors": errors})

    subject = "Заявка с сайта Anima"
    body = (
        f"Имя: {first_name}\n"
        f"Фамилия: {last_name}\n"
        f"Телефон: {phone}\n"
        f"E-mail: {email}\n"
        f"Сообщение:\n{message}"
    )

    if settings.DEBUG:
        print("=" * 50)
        print(f"[FEEDBACK] {subject}")
        print(body)
        print("=" * 50)
    else:
        try:
            send_email(subject, body)
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")

    return JSONResponse({"status": True, "message": "Заявка отправлена!"})
