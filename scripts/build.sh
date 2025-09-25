#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser automatically if environment variables are set
echo "Creating superuser..."
python manage.py createsuperuser_auto

# Seed database with sample data
echo "Seeding database with sample data..."
python manage.py seed_data --movies 100 --users 10