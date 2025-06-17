# Django Real-Time Chat Application Deployment Guide

## Prerequisites

- Ubuntu/Debian VPS with root access
- Python 3.8 or higher
- Redis server
- Nginx (for production)
- Supervisor (for process management)

## Local Development Setup

1. **Clone the repository and navigate to project directory**
   ```bash
   cd /path/to/chat
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Redis**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install redis-server
   sudo systemctl start redis-server
   sudo systemctl enable redis-server
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Or for Channels/WebSocket support:
   ```bash
   daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
   ```

## Production Deployment on VPS

### 1. Server Preparation

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install python3-pip python3-venv redis-server nginx supervisor -y

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 2. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/chat
sudo chown $USER:$USER /var/www/chat

# Clone your application
cd /var/www/chat
# Copy your project files here

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file for production settings
echo "DEBUG=False" > .env
echo "ALLOWED_HOSTS=your-domain.com,your-vps-ip" >> .env
```

### 3. Configure Django for Production

Edit `myproject/settings.py`:
```python
import os
from pathlib import Path

# Add at the top
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Add for static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Collect static files:
```bash
python manage.py collectstatic --noinput
```

### 4. Configure Supervisor for Daphne

Create `/etc/supervisor/conf.d/chat.conf`:
```ini
[program:chat]
command=/var/www/chat/venv/bin/daphne -u /var/www/chat/daphne.sock myproject.asgi:application
directory=/var/www/chat
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/chat/daphne.log
environment=PATH="/var/www/chat/venv/bin"
```

Create log directory:
```bash
sudo mkdir -p /var/log/chat
sudo chown www-data:www-data /var/log/chat
```

### 5. Configure Nginx

Create `/etc/nginx/sites-available/chat`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/chat/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/var/www/chat/daphne.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/chat /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/chat
sudo chmod -R 755 /var/www/chat
```

### 7. Start Services

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start chat
```

### 8. Configure Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

## SSL Certificate (Optional but Recommended)

Install Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Maintenance

### Check Application Logs
```bash
sudo tail -f /var/log/chat/daphne.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Application
```bash
sudo supervisorctl restart chat
```

### Update Application
```bash
cd /var/www/chat
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart chat
```

## Troubleshooting

1. **WebSocket Connection Failed**
   - Check if Redis is running: `redis-cli ping`
   - Verify Nginx configuration includes WebSocket headers
   - Check firewall settings

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check Nginx static files path
   - Verify file permissions

3. **Application Not Starting**
   - Check supervisor logs: `sudo tail -f /var/log/supervisor/supervisord.log`
   - Verify virtual environment path
   - Check Django settings for production

## Security Considerations

1. Always use HTTPS in production
2. Keep SECRET_KEY secure and never commit it
3. Set DEBUG=False in production
4. Regularly update dependencies
5. Configure proper firewall rules
6. Use strong passwords for database and admin accounts