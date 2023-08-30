from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, autoincrement=True, primary_key=True)
    document_path = Column(String)
    summarized_document_path = Column(String, nullable=True)


def insert_documents(document_path_list: list):
    document_list = [Documents(document_path=document_path) for document_path in document_path_list]
