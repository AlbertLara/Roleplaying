from celery import Celery

from app import app

celery = Celery(
    'worker',
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)

@celery.task()
def funct1(arg):
    return False