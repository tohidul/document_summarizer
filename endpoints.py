from app import app

from background_task import summarize_documents_task

@app.route('/summarize', methods=["POST"])
def summarize():
    background_task = summarize_documents_task
    task_id = background_task.delay()
    return task_id