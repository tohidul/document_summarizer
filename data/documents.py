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


