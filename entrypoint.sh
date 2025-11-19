#!/usr/bin/env bash
set -e
python manage.py migrate --no-input 
python manage.py collectstatic --no-input # If this is where it times out, remove it
exec gunicorn orders_sms_service.wsgi:application --bind 0.0.0.0:$PORT