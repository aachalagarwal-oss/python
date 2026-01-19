from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="aachal.agarwal@openxcell.com",
    MAIL_PASSWORD="",
    MAIL_FROM="aachal.agarwal@openxcell.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)
