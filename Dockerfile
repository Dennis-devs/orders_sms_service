# Use official Python slim image for smaller size
FROM python:3.13.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run migrations and collect static files (optional, can be in entrypoint)
RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose port for GAE
EXPOSE 8080

# Run with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "orders_sms_service.wsgi:application"]