"""
Юнит-тесты для Kafka producer.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.kafka_producer import send_to_kafka

@patch('app.kafka_producer.producer')
def test_send_to_kafka(mock_producer):
    """Тестирование отправки сообщения в Kafka."""
    send_to_kafka("test_topic", {"key": "value"})
    mock_producer.send.assert_called_once_with("test_topic", {"key": "value"})
    mock_producer.flush.assert_called_once()