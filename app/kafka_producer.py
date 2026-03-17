"""
Kafka Producer Module

This module handles sending messages to Kafka topics.
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
    Send a message to the specified Kafka topic.

    Args:
        topic (str): The Kafka topic to send the message to.
        message (dict): The message payload as a dictionary.
    """
    try:
        producer.send(topic, message)
        producer.flush()
        logger.info(f"Message sent to Kafka topic '{topic}': {message}")
    except Exception as e:
        logger.error(f"Failed to send message to Kafka: {str(e)}")
        raise