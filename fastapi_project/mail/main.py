from fastapi import BackgroundTasks, FastAPI,HTTPException,status
from typing import Annotated

app = FastAPI()


#fire and forget function
def send_email_notiification(email:str,message:str):
   print(f"sending '{message}' to {email}")



@app.post("/send-notification/{email}",status_code=status.HTTP_201_CREATED)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_notiification,email, message="some notification")
    return {"message": "Notification sent in the background"}



# send_notification()   →  synchronous, client waits
# send_email_notiification() → asynchronous, fire-and-forget
