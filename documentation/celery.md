# Celery
- Used to distribute tasks 
- Example:
- In a normal for loop, you iterate and have to wait for a function to complete in order to move to next iteration
  - ie. 0, 1, 2, 3 all handled by the same single CPU core/process/thread
```
for i in range(0,20):
    do somthing 1... # assigned to Single Core
    do somthing 2... # have to wait for 1 to finish before moving on
```
- With celery you can assign task_name to multiple processes/threads at the same time and applying concurrency
```
for i in range(0,20):
    task_name.delay(0) # assigned to Worker A
    task_name.delay(1) # assigned to Worker B
    ...
```
- Allows performance increase when dealing with multiple requests

# Getting Started

## Start RabbitMQ 
- RabbitMQ is required by celery as a message broker
- Also used as backend/storage to celery service perform tasks assigned by celery
```
docker run -d -p 5672:5672 rabbitmq
or 
npm run rabbit
```

## WORKERS Run in foreground
```
celery -A celery_tasks worker --loglevel=info --pool=eventlet --autoscale=1,12 -O fair
```

## WORKERS Run in background
```
celery -A celery_tasks multi start worker1 
```

## WORKERS Stop
```
celery -A celery_tasks multi stop worker1 
```

## BEATS
- Used for Scheduled tasks
```
celery -A celery_beats multi start beat-worker -B --loglevel=info --autoscale=1,12 -O fair
```

## FLOWER
- Used for monitoring celery tasks
```
flower -A celery_tasks --port=5555
or
npm run flower
```

# Recommendation Articles
- https://denibertovic.com/posts/celery-best-practices/
  - Use a database
  - Use Queues
    - celery worker -E -l INFO -n workerA -Q for_task_A
    - celery worker -E -l INFO -n workerB -Q for_task_B
  - Use Priority workers
  - Use Celery's error handling mechanisms
  - Use Flower
  - Keep track of results only if you really need them
  - Don't pass Database/ORM objects to tasks

- https://www.caktusgroup.com/blog/2014/09/29/celery-production/
# Default queue
python manage.py celery worker -Q celery
# High priority queue. 10 workers
python manage.py celery worker -Q high -c 10
# Low priority queue. 2 workers
python manage.py celery worker -Q low -c 2
# Beat process
python manage.py celery beat

# Heavy tasks
https://www.distributedpython.com/2018/10/26/celery-execution-pool/

