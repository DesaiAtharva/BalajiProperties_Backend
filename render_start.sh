#!/usr/bin/env bash
# exit on error
set -o errexit

# Run migrations
python manage.py migrate

# Create superuser automatically if it doesn't exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin1').exists() or User.objects.create_superuser('admin1', 'admin@example.com', '12345678')"

# Seed property data
python seed_properties.py

# Start Gunicorn
gunicorn core.wsgi:application
