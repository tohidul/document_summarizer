from flask import Flask
from data import init_db, create_table_if_not_exist, session

from celery import Celery


app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')

init_db(app.config)
create_table_if_not_exist(session)

def _make_celery_app(flask_app):
    app = Celery(__name__)
    if 'CELERY_CONFIG' in flask_app.config:
        app.conf.update(flask_app.config.get('CELERY_CONFIG', {}))
    else:
        app.conf.update(flask_app.config)
    return app


celery_app = _make_celery_app(app)




import endpoints

if __name__ == '__main__':
    app.run()
