# My Personal Flask Blog

A personal blog application built with Flask for lifestyle, technology, and educational posts.

## Features

- User registration and authentication
- Create, read, and manage blog posts
- Comment system
- Tagging system for posts
- Author pages
- Category browsing

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize the database: `flask db init` (if using Flask-Migrate)
3. Run the application: `python main.py`

## Configuration

The application can be configured using environment variables:
- `SECRET_KEY`: Secret key for security (defaults to a development key)
- `DATABASE_URL`: Database URL (defaults to SQLite)
- `IP`: Host IP address (defaults to 127.0.0.1)
- `PORT`: Port number (defaults to 8080)
