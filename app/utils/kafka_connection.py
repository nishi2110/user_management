from quixstreams import Application

import logging

from settings.config import settings
from app.models.user_model import User


class KafkaClient:
    def __init__(self, broker_address: str, consumer_group: str, auto_offset_reset: str='latest'):
        self.kafka_app = Application(broker_address=broker_address, consumer_group=consumer_group, auto_offset_reset=auto_offset_reset)
    
    def produce(self, user: User, msg_type: str, msg: str):
        try:
            kafka_topic = f'{user.id}'
            with self.kafka_app.get_producer() as producer:
                producer.produce(topic=kafka_topic,
                                key=msg_type,
                                value=msg)
                logging.info(f"message for {kafka_topic} produced.")
        except Exception as e:
            logging.error(e)

    def consume(self, user: User):
        try:
            kafka_topic = f'{user.id}'
            with self.kafka_app.get_consumer() as consumer:
                consumer.subscribe([kafka_topic])
                msg = consumer.poll(5)
                if msg.error() is not None:
                    logging.error(Exception(msg.error()))
                consumer.store_offsets(msg)
                return msg.key().decode('utf8'), msg.value().decode('utf8')
        except Exception as e:
            logging.error(e)

kafka_client = KafkaClient(settings.kafka_broker_address, settings.server_name, 'latest')
