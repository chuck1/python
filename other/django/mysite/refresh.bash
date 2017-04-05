#!/bin/bash
python manage.py makemigrations
python manage.py migrate
sudo service apache2 restart
