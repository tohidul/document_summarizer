from sqlalchemy import Column, Integer, String

from data import Base, session

class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, autoincrement=True, primary_key=True)
    document_path = Column(String)
    summarized_document_path = Column(String, nullable=True)


def insert_documents(document_path_list: list):
    document_list = [Documents(document_path=document_path) for document_path in document_path_list]
    session.bulk_save_objects(document_list)
    session.commit()


def get_documents():
    query_result = session.query(Documents.id, Documents.document_path, Documents.summarized_document_path).all()
    list_of_documents = []
    for result in query_result:

    return

