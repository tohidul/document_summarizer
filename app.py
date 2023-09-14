from flask import Flask, request
from data import init_db, create_table_if_not_exist, session
from data.documents import insert_documents
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


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/summarize', methods=["POST"])
def summarize():
    return 'Hello World!'

@app.route('/add_documents', methods=["POST"])
def add_documents():
    list_of_docs = request.form.getlist("document_list")
    response = {
        "document_inserted": False
    }
    if not list_of_docs:
        return response
    try:
        insert_documents(list_of_docs)
        response["document_inserted"] = True
        return response
    except:
        return response

@app.route('/get_summary', methods=["GET"])
def get_summary():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
