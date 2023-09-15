from app import celery_app
from data import documents
from summarize import filter_tokens, count_word_frquency, weighing_sentences, get_summarized_text
import spacy
import os
import time
import logging

nlp = spacy.load('en_core_web_sm')


def summarize_document(document_path):
    with open(document_path, "r") as document_file:
        document_content = document_file.read()
    document = nlp(document_content)

    keywords = filter_tokens(document)
    keyword_frequencies = count_word_frquency(keywords)
    sentence_strengths = weighing_sentences(document, keyword_frequencies)
    summarized_text = get_summarized_text(sentence_strengths, number_of_sentence=3)
    directory_path_of_file = os.path.abspath(os.path.dirname(document_path))
    document_file_name = os.path.basename(document_path)
    document_file_name_without_extension = document_file_name.split(".")[0]
    document_summary_file_name = document_file_name_without_extension+"_summmarized.txt"
    document_summary_file_path = os.path.join(directory_path_of_file, document_summary_file_name)
    with open(document_summary_file_path, "w") as summarized_file_path:
        summarized_file_path.write(summarized_text)

    return document_summary_file_path


@celery_app.task
def summarize_documents_task():
    start_time = time.time()
    list_of_documnents = documents.get_documents()
    list_of_summarized_documents = []
    total = len(list_of_documnents)
    processed = 0
    for document in list_of_documnents:
        summarized_document_path = summarize_document(document["document_path"])
        summarized_document_info = {
            "id": document["document_id"],
            "summarized_document_path":  summarized_document_path
        }
        list_of_summarized_documents.append(summarized_document_info)
        processed += 1
        if processed % 100 == 0:
            summarize_documents_task.update_state(state="PROGRESS", meta={"processed": processed, "total":total})


    documents.add_summarized_document_path(list_of_summarized_documents)
    response = {
        "processed": processed,
        "total": total
    }
    end_time = time.time()

    logging.info("time taken to summarize all documents: {} seconds".format(end_time-start_time))
    return response

@celery_app.task
def get_documents():





