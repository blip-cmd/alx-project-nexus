#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

# Create superuser automatically if environment variables are set
echo "Creating superuser..."
python manage.py createsuperuser_auto || echo "Superuser creation skipped or already exists"

# Seed database with sample data (optional, skip if it fails)
echo "Seeding database with sample data..."
python manage.py seed_data --movies 100 --users 10 || echo "Data seeding skipped or failed"

echo "Build completed successfully!"