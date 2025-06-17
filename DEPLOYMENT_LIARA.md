# Deployment Guide for Liara and Similar Platforms

## Known Issues with WebSockets

Some hosting platforms (including Liara) may have limitations with WebSocket connections:
- WebSocket connections may timeout
- Long-running connections may be terminated
- The container may receive SIGTERM signals

## Solution: Fallback Mode

The chat application now includes a fallback mechanism:

1. **WebSocket Mode** (preferred): Real-time messaging when WebSockets work
2. **HTTP Fallback Mode**: Regular form submission when WebSockets fail

## Features in Fallback Mode

- ✅ Messages are sent and stored
- ✅ Chat history is preserved
- ⚠️ No real-time updates (users need to refresh)
- ✅ Auto-refresh every 10 seconds when WebSocket fails

## Deployment Options

### Option 1: Try with WebSocket Support (Default)

Deploy normally and the app will automatically fall back if WebSockets don't work.

### Option 2: Disable WebSockets Entirely

If you want to disable WebSockets completely:

1. Set environment variable:
   ```
   DJANGO_SETTINGS_MODULE=myproject.settings_no_websocket
   ```

2. Or modify your Dockerfile:
   ```dockerfile
   ENV DJANGO_SETTINGS_MODULE=myproject.settings_no_websocket
   ```

## Debugging WebSocket Issues

1. Check browser console for WebSocket errors
2. Look for the yellow warning banner in the chat interface
3. Check container logs for SIGTERM signals

## Platform-Specific Notes

### Liara
- WebSockets may work intermittently
- Container restarts are common
- Use the fallback mode for reliability

### Heroku
- WebSockets generally work well
- No special configuration needed

### DigitalOcean App Platform
- WebSockets supported
- May need to configure health checks

## Recommended Configuration

For maximum compatibility, the app now:
1. Attempts WebSocket connection
2. Falls back to HTTP if WebSocket fails
3. Shows user-friendly warnings
4. Auto-refreshes in fallback mode

This ensures the chat works on any platform!