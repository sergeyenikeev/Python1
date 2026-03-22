"""Redis helpers for caching processed text results."""

import hashlib
import logging
import os
from typing import Any, Optional

import redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

DEFAULT_REDIS_URL = "redis://redis:6379/0"
DEFAULT_CACHE_TTL_SECONDS = 3600

redis_client: Optional[redis.Redis] = None


def get_redis_url() -> str:
    """Return the configured Redis connection URL."""
    return os.getenv("REDIS_URL", DEFAULT_REDIS_URL)


def get_cache_ttl_seconds() -> int:
    """Return cache TTL in seconds."""
    ttl = os.getenv("REDIS_CACHE_TTL_SECONDS", str(DEFAULT_CACHE_TTL_SECONDS))
    return int(ttl)


def get_redis_client() -> redis.Redis:
    """Create the Redis client lazily to keep imports side-effect free."""
    global redis_client

    if redis_client is None:
        redis_client = redis.Redis.from_url(get_redis_url(), decode_responses=True)
        logger.info("Redis client initialized.")

    return redis_client


def build_cache_key(text: str) -> str:
    """Build a stable Redis key for the provided text payload."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"processed_text:{digest}"


def get_cached_result(text: str) -> Optional[str]:
    """Return the cached processed result when available."""
    try:
        cached_result = get_redis_client().get(build_cache_key(text))
    except RedisError:
        logger.exception("Failed to read from Redis cache.")
        return None

    if cached_result is None:
        logger.info("Redis cache miss for text payload.")
    else:
        logger.info("Redis cache hit for text payload.")

    return cached_result


def set_cached_result(text: str, result: str) -> None:
    """Persist the processed result in Redis with a TTL."""
    try:
        get_redis_client().setex(build_cache_key(text), get_cache_ttl_seconds(), result)
        logger.info("Processed result cached in Redis.")
    except RedisError:
        logger.exception("Failed to write to Redis cache.")


def inspect_cache(text: str) -> dict[str, Any]:
    """Return cached value and TTL for the provided text."""
    key = build_cache_key(text)
    try:
        client = get_redis_client()
        value = client.get(key)
        ttl = client.ttl(key)
    except RedisError:
        logger.exception("Failed to inspect Redis cache.")
        return {"error": "Redis unavailable"}

    if ttl in (-2, None):
        ttl = None
    if ttl == -1:
        ttl = None

    return {"key": key, "value": value, "ttl": ttl}
