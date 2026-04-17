import os


class Settings:
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Google reCAPTCHA v2
    # Тестовые ключи Google (работают на localhost)
    # Для продакшена задать через переменные окружения
    RECAPTCHA_SITE_KEY: str = os.getenv(
        "RECAPTCHA_SITE_KEY", "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    )
    RECAPTCHA_SECRET_KEY: str = os.getenv(
        "RECAPTCHA_SECRET_KEY", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    )

    # Email (SMTP)
    # Для Mail.ru: smtp.mail.ru:465
    # Для Yandex:  smtp.yandex.ru:465
    # Для Gmail:   smtp.gmail.com:465
    # EMAIL_PASSWORD — пароль приложения (не пароль от почты!)
    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", "465"))
    EMAIL_USER: str = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    FEEDBACK_EMAIL: str = os.getenv("FEEDBACK_EMAIL", "anima.market@mail.ru")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "anima.market@mail.ru")


settings = Settings()
