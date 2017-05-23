
python manage.py dumpdata kitchen > temp_kitchen.json
python manage.py dumpdata lit > temp_lit.json
python manage.py dumpdata task > temp_task.json
python manage.py dumpdata climb > temp_climb.json

python manage.py flush

python manage.py loaddata temp_kitchen.json temp_lit.json temp_task.json

