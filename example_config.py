from urllib.parse import quote

DB_CONFIG = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': 5432,
    'username': 'postgres',
    'password': 'envizemssqlpassword123@@',
    'database': 'document_summarizer',
    'query': {'client_encoding': 'utf8'}
}

CELERY_CONFIG = {
     'CELERY_BROKER_URL': 'memory://localhost/',
     'BROKER_URL': 'amqp://test_user:test_user@localhost:5672/summarizer',
     'CELERY_RESULT_BACKEND': 'db+postgresql://postgres:%s@localhost:5432/document_summarizer' % quote('envizemssqlpassword123@@')
}

