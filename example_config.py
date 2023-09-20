from urllib.parse import quote


DB_CONFIG = {
    'drivername': '<db_driver>',
    'host': '<host_name>',
    'port': '<port>',
    'username': '<db_user_name>',
    'password': '<db_password>',
    'database': '<db_name>',
    'query': {'client_encoding': 'utf8'}
}


#Used rabbitmq as broker. You can also use redis
#Both db table or redis can be used to store celery result
CELERY_CONFIG = {
     'CELERY_BROKER_URL': 'memory://<broker_host>/',
     'BROKER_URL': 'amqp://<rabbitmq_user>:<rabbitmq_password>@<broker_host>:5672/<virtual_host_name>',
     'CELERY_RESULT_BACKEND': '<celery backed config>'
}

