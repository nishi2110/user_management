from celery import Celery

from settings.config import settings

app = Celery('app', 
             broker=f'kafka://{settings.kafka_broker_address}', 
             backend='db+postgresql://user:password@postgres/myappdb'
             )

app.autodiscover_tasks(['app.utils'])

app.conf.update(broker_connection_retry_on_startup=True)
