#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py syncdb

python manage.py loaddata temp.json
