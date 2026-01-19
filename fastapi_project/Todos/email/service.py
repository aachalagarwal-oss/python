from fastapi_mail import FastMail, MessageSchema
from .config import conf

async def send_email_notification(email: str, message: str):
    mail = FastMail(conf)

    email_message = MessageSchema(
        subject="Welcome mail",
        recipients=[email],
        body=message,
        subtype="plain"
    )

    await mail.send_message(email_message)
