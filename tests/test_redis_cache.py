"""Unit tests for Redis cache helpers."""

from unittest.mock import MagicMock, patch

from app.redis_cache import build_cache_key, get_cached_result, set_cached_result


@patch("app.redis_cache.get_redis_client")
def test_get_cached_result(mock_get_client):
    """Cached result should be fetched by the generated Redis key."""
    mock_client = MagicMock()
    mock_client.get.return_value = "CACHED TEXT"
    mock_get_client.return_value = mock_client

    result = get_cached_result("hello")

    assert result == "CACHED TEXT"
    mock_client.get.assert_called_once_with(build_cache_key("hello"))


@patch("app.redis_cache.get_cache_ttl_seconds", return_value=123)
@patch("app.redis_cache.get_redis_client")
def test_set_cached_result(mock_get_client, mock_get_ttl):
    """Cached result should be stored with the configured TTL."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    set_cached_result("hello", "HELLO")

    mock_client.setex.assert_called_once_with(build_cache_key("hello"), 123, "HELLO")
