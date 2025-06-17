# Django Real-Time Chat Application

A real-time chat application built with Django Channels, Redis, and WebSockets. Users can find each other using unique 8-character IDs and engage in private one-on-one conversations.

## Features

- 🔐 User authentication (registration/login)
- 🆔 Unique 8-character ID for each user
- 💬 Real-time messaging with WebSockets
- 👥 Private one-on-one chat rooms
- 📝 Persistent message history
- 📊 Unread message indicators
- 📱 Responsive Bootstrap UI

## Prerequisites

- Python 3.8+
- Redis server (for WebSocket channel layer)

## Quick Start

### Option 1: Using the run script (Recommended)

```bash
# Make sure Redis is installed and running
./run_dev.sh
```

The script will:
- Create/activate virtual environment
- Install all dependencies
- Check Redis connection
- Run database migrations
- Start the development server

### Option 2: Manual setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and start Redis:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   sudo systemctl start redis-server
   
   # macOS
   brew install redis
   brew services start redis
   
   # Or run manually
   redis-server
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   # With full WebSocket support
   daphne -b 127.0.0.1 -p 8000 myproject.asgi:application
   
   # Or standard Django server (limited WebSocket support)
   python manage.py runserver
   ```

## Usage

1. **Register/Login:** Create a new account or login
2. **Get Your ID:** Your unique 8-character ID is displayed in the navbar
3. **Find Users:** Use the "Find User" page to connect with others by their ID
4. **Start Chatting:** Real-time messages with typing indicators

## Project Structure

```
chat/
├── myproject/          # Django project settings
├── main/              # Main application
│   ├── models.py      # UserProfile, ChatRoom, Message models
│   ├── views.py       # View logic
│   ├── consumers.py   # WebSocket consumers
│   ├── routing.py     # WebSocket routing
│   └── templates/     # HTML templates
├── static/            # CSS and static files
├── venv/             # Virtual environment
├── run_dev.sh        # Development server script
└── DEPLOYMENT.md     # Production deployment guide
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin` to:
- Manage users and profiles
- View chat rooms and messages
- Monitor application data

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to a VPS with Nginx, Supervisor, and SSL.

## Troubleshooting

### Redis Connection Error
Make sure Redis is installed and running:
```bash
redis-cli ping  # Should return PONG
```

### WebSocket Connection Failed
- Ensure you're using Daphne (not just `runserver`)
- Check browser console for errors
- Verify CHANNEL_LAYERS configuration in settings.py

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use HTTPS for production deployment
- Keep Redis secured (bind to localhost only)

## License

This project is open source and available under the MIT License.# chat
# chat
