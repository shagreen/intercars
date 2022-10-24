#!/bin/bash
echo "Migrations"
python3 /app/manage.py migrate
echo "starting"
python3 /app/manage.py runserver 0.0.0.0:8000
#tail -F anything