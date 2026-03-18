"""Kafka producer helpers."""

import json
import logging
import os
from typing import Any, Optional

from kafka import KafkaProducer

logger = logging.getLogger(__name__)

DEFAULT_KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"
producer: Optional[KafkaProducer] = None


def get_kafka_bootstrap_servers() -> list[str]:
    """Return Kafka bootstrap servers from the environment."""
    servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", DEFAULT_KAFKA_BOOTSTRAP_SERVERS)
    return [server.strip() for server in servers.split(",") if server.strip()]


def get_kafka_producer() -> KafkaProducer:
    """Create the producer lazily so imports stay side-effect free."""
    global producer

    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=get_kafka_bootstrap_servers(),
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )
        logger.info("Kafka producer initialized.")

    return producer


def send_to_kafka(topic: str, message: dict[str, Any]) -> None:
    """Publish a message to the requested Kafka topic."""
    active_producer = producer or get_kafka_producer()
    try:
        active_producer.send(topic, message)
        active_producer.flush()
        logger.info("Message sent to Kafka topic '%s'.", topic)
    except Exception:
        logger.exception("Failed to send message to Kafka.")
        raise
