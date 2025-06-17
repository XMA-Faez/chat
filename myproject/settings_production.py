# Production settings example for external Redis
import os

# For Redis Cloud or external Redis service
REDIS_URL = os.environ.get('REDIS_URL', None)

if REDIS_URL:
    # Parse Redis URL for services like Redis Cloud
    import urllib.parse
    url = urllib.parse.urlparse(REDIS_URL)
    
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [{
                    "host": url.hostname,
                    "port": url.port,
                    "password": url.password,
                }],
            },
        },
    }
else:
    # Fallback to localhost
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    }