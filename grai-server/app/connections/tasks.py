from celery import shared_task

@shared_task
def add(x, y):
    print("Hello task running")
    print(x + y)
    # return x + y