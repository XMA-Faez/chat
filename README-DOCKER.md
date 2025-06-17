# Running the Chat App with Docker

This guide explains how to run the Django chat application using Docker, which includes Redis and all necessary dependencies.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Application: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - Default admin credentials: `admin` / `admin123`

## Docker Commands

### Start the application
```bash
# Run in the foreground (see logs)
docker-compose up

# Run in the background
docker-compose up -d

# Rebuild after code changes
docker-compose up --build
```

### Stop the application
```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (deletes database)
docker-compose down -v
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f redis
```

### Access the Django shell
```bash
docker-compose exec web python manage.py shell
```

### Create a new superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Run migrations
```bash
docker-compose exec web python manage.py migrate
```

## What's Included

The Docker setup includes:

- **Web container**: Django application with Channels/Daphne
- **Redis container**: For WebSocket channel layer
- **Automatic migrations**: Database migrations run on startup
- **Default admin user**: Username `admin`, password `admin123`
- **Volume persistence**: Database and Redis data persist between restarts

## Development Workflow

1. Make code changes
2. Rebuild and restart:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

## Troubleshooting

### Container won't start
Check logs:
```bash
docker-compose logs web
```

### WebSocket connection issues
Ensure both containers are running:
```bash
docker-compose ps
```

### Reset everything
```bash
docker-compose down -v
docker-compose up --build
```

## Production Considerations

For production deployment:

1. Change the default admin password
2. Set `DEBUG=False` in docker-compose.yml
3. Use environment variables for secrets
4. Add nginx container for static files
5. Use PostgreSQL instead of SQLite