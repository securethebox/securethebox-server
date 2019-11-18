from celery_tasks import add
import time

if __name__ == "__main__":
    r = add.delay(1,1)
    while not r.ready():
        print("not ready yet...")
        time.sleep(0.1)
    print(r.get())


