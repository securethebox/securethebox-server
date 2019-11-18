from celery import Celery
from celery.schedules import crontab

app = Celery('celery_tasks', backend='db+postgresql://airflow:airflow@postgres:5432/airflow', broker='redis://redis:6379/0')

@app.task
def add(x, y):
    return x + y
