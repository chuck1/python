
To avoid conflict with other celery instances, create new rabbitmq vhost

    rabbitmqctl add_vhost host1
    rabbitmqctl set_permissions -p host1 guest '.*' '.*' '.*'

    celery -A tasks worker -l info -b amqp://guest@localhost/host1


In tasks.py, we use the same amqp uri as the broker when we create our app

