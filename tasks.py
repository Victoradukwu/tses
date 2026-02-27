import time

from celery_app import app as celery_app
from django.conf import settings  # noqa: F401


@celery_app.task(name="tasks.addition")
def add_numbers(a: int, b: int) -> int:
    x = time.time()
    time.sleep(10)
    y = time.time()
    print(f"HHHHJJJ: {y - x}")
    return a + b
