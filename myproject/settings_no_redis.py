# Settings for running without Redis (no real-time features)
# Chat will still work but without real-time updates

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Note: InMemoryChannelLayer only works with a single process
# and doesn't persist messages between restarts