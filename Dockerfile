# Use official Python slim image for smaller size
FROM python:3.13.7-slim

# Set working directory
WORKDIR /app

# install dependencies into a virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"


# Install system dependencies (for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ENV SECRET_KEY=os.environ.get('SECRET_KEY')
# ENV DATABASE_URL=os.environ.get('DATABASE_URL')

# Copy the rest of the app
COPY . .
RUN chmod -R 777 /app
# Run migrations and collect static files (optional, can be in entrypoint)
# RUN python manage.py makemigrations && python manage.py migrate
# RUN python manage.py collectstatic --noinput
# Copy the script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Tell Docker to run this script when the container starts
CMD ["/app/entrypoint.sh"] 


# Expose port 
# EXPOSE 8080

# Run with Gunicorn for production
# CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "2", "orders_sms_service.wsgi:application"]
# CMD ["/bin/sh", "-c", "python manage.py migrate --no-input && gunicorn orders_sms_service.wsgi:application --bind 0.0.0.0:$PORT --timeout 120"]

