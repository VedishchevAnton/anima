import os


class Settings:
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Google reCAPTCHA v2
    # Тестовые ключи Google (работают на localhost)
    # Продакшен (animacoffee.pro): 6Lf4qscsAAAAANMawXOY9pQVXhwTTIXkqLQC-_Ue / 6Lf4qscsAAAAAAwyN7zw0fJc_3Rb6fHxNTvdTrTC
    RECAPTCHA_SITE_KEY: str = os.getenv(
        "RECAPTCHA_SITE_KEY", "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    )
    RECAPTCHA_SECRET_KEY: str = os.getenv(
        "RECAPTCHA_SECRET_KEY", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    )

    # Yandex Maps
    # Получить ключ: https://developer.tech.yandex.ru/
    YANDEX_MAP_API_KEY: str = os.getenv("YANDEX_MAP_API_KEY", "40546000-1e1e-4551-91b5-635af6c5c74f")

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
