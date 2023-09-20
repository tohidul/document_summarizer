from app import app
from flask import request
from background_task import summarize_documents_task, get_documents, summarize, update_db
from data.documents import get_document_count, get_summarized_document_text
from celery import chain, group
from data.documents import insert_documents


@app.route('/summarize', methods=["POST"])
def summarize_documents():
    number_of_concurrent_task = request.form.get("number_of_concurrent_task", type=int, default=1)
    total_documents = get_document_count()
    if total_documents < number_of_concurrent_task:
        number_of_concurrent_task = total_documents
    if number_of_concurrent_task>1:
        background_task = chain(get_documents.s(chunk_size=total_documents//number_of_concurrent_task),
                       group(summarize.s(index=i) for i in range(number_of_concurrent_task)),
                       update_db.s())
    else:
        background_task = summarize_documents_task
    task_id = background_task.apply_async()
    response = {
        "task_id": str(task_id)
    }
    return response


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
    list_of_document_ids = request.form.getlist("document_id_list")
    result = get_summarized_document_text(list_of_document_ids)
    return result
