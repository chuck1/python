#!/bin/bash
python manage.py dumpdata -e contenttypes -e auth.Permission > temp.json
python manage.py sqlclear kitchen | python manage.py dbshell
python manage.py sqlflush | python manage.py dbshell

