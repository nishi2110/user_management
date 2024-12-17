from settings.config import settings

#broker_url = f'kafka://{settings.kafka_broker_address}'
#result_backend = 'db+postgresql+asyncpg://user:password@postgres/myappdb:5432/myappdb'
task_serializer = 'json'  # Task serialization format
result_serializer = 'json'  # Result serialization format
accept_content = ['json']
broker_connection_retry_on_startup = True
timezone = 'UTC'
enable_utc = True
