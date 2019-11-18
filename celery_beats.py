from celery import Celery
from celery.schedules import crontab
import random 

app = Celery('celery_beats', backend='db+postgresql://airflow:airflow@postgres:5432/airflow', broker='redis://redis:6379/0')

randomNumber = str(random.choice([1, 4, 8, 10, 3]))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    
    sender.add_periodic_task(1.0, test.s(randomNumber), name='add every 10')
    sender.add_periodic_task(1.0, test.s(randomNumber), name='add every 10')
    sender.add_periodic_task(1.0, test.s(randomNumber), name='add every 10')
    sender.add_periodic_task(1.0, test.s(randomNumber), name='add every 10')
    sender.add_periodic_task(1.0, test.s(randomNumber), name='add every 10')
    sender.add_periodic_task(1.0, test.s(randomNumber), name='add every 10')

@app.task
def test(arg):
    for i in range(0,10):
        print(arg)