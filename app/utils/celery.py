from celery import Celery

from settings.config import settings

app = Celery('myapp',
             broker=f'kafka://{settings.kafka_broker_address}',
             backend='db+postgresql://user:password@postgres/myappdb')

app.autodiscover_tasks(['app.utils'])

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)