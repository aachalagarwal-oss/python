FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app_tasks /app/app_tasks

CMD ["uvicorn", "app_tasks.main:app", "--host", "0.0.0.0", "--port", "8000"]
