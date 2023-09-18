from app import app
from flask import request
from background_task import summarize_documents_task, get_documents, summarize, update_db
from data.documents import get_document_count
from celery import chain, group


@app.route('/summarize', methods=["POST"])
def summarize_documents():
    number_of_concurrent_task = request.form.get("number_of_concurrent_task", type=int, default=1)
    total_documents = get_document_count()
    if total_documents < number_of_concurrent_task:
        number_of_concurrent_task = total_documents
    if number_of_concurrent_task>1:
        result = chain(get_documents.s(chunk_size=number_of_concurrent_task),
                       group(summarize.s(index=i) for i in range(number_of_concurrent_task)),
                       update_db.s())
        task_id = result.apply_async()
        response = {
            "task_id": str(task_id)
        }
    else:

        background_task = summarize_documents_task
        result = background_task.delay()
        response = {
            "task_id": result.task_id
        }
    return response
