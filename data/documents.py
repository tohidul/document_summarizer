from sqlalchemy import Column, Integer, String, exc
from data import Base, session


class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, autoincrement=True, primary_key=True)
    document_path = Column(String)
    summarized_document_path = Column(String, nullable=True)


def insert_documents(document_path_list: list) -> bool:
    try:
        document_list = [Documents(document_path=document_path) for document_path in document_path_list]
        session.bulk_save_objects(document_list)
        session.commit()
        return True
    except exc.SQLAlchemyError:
        return False


def get_documents() -> list:
    query_result = session.query(Documents.id, Documents.document_path, Documents.summarized_document_path).all()
    list_of_documents = []
    for result in query_result:
        document = {
            "document_id": result.id,
            "document_path": result.document_path,
            "summarized_document_path": result.summarized_document_path
        }
        list_of_documents.append(document)

    return list_of_documents


def add_summarized_document_path(list_of_document_id_to_summarized_path_dictionary: list) -> bool:
    try:
        session.bulk_update_mappings(Documents, list_of_document_id_to_summarized_path_dictionary)
        session.commit()
        return True
    except exc.SQLAlchemyError:
        return False


def get_document_count() -> int:
    row_count = session.query(Documents).count()
    return row_count


def get_summarized_document_text(list_of_document_ids):
    query_result = session.query(Documents.id, Documents.summarized_document_path).filter(Documents.id.in_(list_of_document_ids)).all()

    summarized_text_list = []

    for result in query_result:
        summarized_text_path = result.summarized_document_path
        if summarized_text_path:
            text, error_message = get_text_from_file_path(summarized_text_path)
        else:
            text = None,
            error_message = "missing summarized text path in db"

        summary = {
            "document_id": result.id,
            "summarized_text": text,
            "error_message": error_message
        }
        summarized_text_list.append(summary)
    return summarized_text_list


def get_text_from_file_path(text_path):
    text = ""
    error_message = None

    try:
        with open(text_path, "r") as text_file:
            text = text_file.read()
    except IOError:
        error_message = "Could not read sumnmarized text file"

    return text, error_message
