# LifeOS — Production Deployment & Operator Guide

This document provides detailed instructions for deploying and running **LifeOS** in production environments.

## System Prerequisites

- Python 3.7+ (Python 3.8 / 3.9 recommended)
- SQLite 3.30+
- Modern Web Browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

## Environment Variables (.env)

Create a `.env` file in the project root:

```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your_random_production_secret_key_here
JWT_SECRET_KEY=your_random_jwt_secret_key_here
DATABASE_URL=sqlite:///data/lifeos.db
```

## Production WSGI Server Setup (Gunicorn)

Install Gunicorn:

```bash
pip install gunicorn
```

Run application with 4 worker processes:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Systemd Service Configuration (/etc/systemd/system/lifeos.service)

```ini
[Unit]
Description=LifeOS Web Application Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/lifeos
Environment="PATH=/var/www/lifeos/venv/bin"
ExecStart=/var/www/lifeos/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
```
