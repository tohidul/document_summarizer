from app import app

from background_task import summarize_documents_task

@app.route('/summarize', methods=["POST"])
def summarize():
    background_task = summarize_documents_task
    result = background_task.delay()
    response = {
        "task_id": result.task_id
    }
    return response