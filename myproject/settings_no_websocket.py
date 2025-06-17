# Settings for platforms that don't support WebSockets
# Import all settings from base settings file
from .settings import *

# Disable WebSocket functionality
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Note: With this configuration, chat will work but without real-time updates
# Users need to refresh the page to see new messages