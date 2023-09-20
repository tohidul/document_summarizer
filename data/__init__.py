from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
session = sessionmaker()

Base = declarative_base()
session = scoped_session(session)
Base.query = session.query_property()


def _make_engine(config):
    engine = create_engine(URL(**config["DB_CONFIG"]), echo=True)
    return engine


def init_db(config):
    session.configure(bind=_make_engine(config))


def create_table_if_not_exist(session):
    Base.metadata.create_all(bind=session.get_bind())



