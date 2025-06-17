#!/bin/bash

# Run development server with Redis check

echo "Django Chat Application Development Server"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
echo "Installing/updating requirements..."
pip install -q -r requirements.txt

# Check if Redis is running
echo "Checking Redis server..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Redis is not running!"
    echo "Please install and start Redis:"
    echo "  Ubuntu/Debian: sudo apt-get install redis-server && sudo systemctl start redis-server"
    echo "  macOS: brew install redis && brew services start redis"
    echo "  Or run: redis-server"
    exit 1
else
    echo "✓ Redis is running"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Start the development server
echo ""
echo "Starting Django Channels development server..."
echo "Access the application at: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

# Run with Daphne for WebSocket support
daphne -b 127.0.0.1 -p 8000 myproject.asgi:application