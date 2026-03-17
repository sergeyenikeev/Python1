"""
Модуль Kafka Producer

Этот модуль обрабатывает отправку сообщений в топики Kafka.
"""

import logging
from kafka import KafkaProducer
import json

logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(topic: str, message: dict):
    """
    Отправить сообщение в указанный топик Kafka.

    Args:
        topic (str): Топик Kafka для отправки сообщения.
        message (dict): Полезная нагрузка сообщения в виде словаря.
    """
    try:
        producer.send(topic, message)
        producer.flush()
        logger.info(f"Сообщение отправлено в топик Kafka '{topic}': {message}")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение в Kafka: {str(e)}")
        raise