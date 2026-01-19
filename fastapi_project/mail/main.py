from fastapi import BackgroundTasks, FastAPI,HTTPException,status
from typing import Annotated

from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
import asyncio


app = FastAPI()



conf = ConnectionConfig(
    MAIL_USERNAME="aachal.agarwal@openxcell.com",
    MAIL_PASSWORD="vohx jqgb etfg tuse",
    MAIL_FROM="aachal.agarwal@openxcell.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)




#fire and forget function
async def send_email_notiification(email:str,message:str):
    mail=FastMail(conf)
    email_message=MessageSchema(
        subject="notification",
        recipients=[email],
        body=message,
        subtype="plain"
    )

    #.send_message() is the function that actually sends the email to the SMTP server.
    await mail.send_message(email_message)



@app.post("/send-notification/{email}",status_code=status.HTTP_201_CREATED)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_notiification,email, message="some notification")
    return {"message": "Notification sent in the background"}



# send_notification()   →  synchronous, client waits
# send_email_notiification() → asynchronous, fire-and-forget
   