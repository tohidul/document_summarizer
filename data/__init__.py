from sqlalchemy import create_engine, URL


def _make_engine(config):
    engine = create_engine(URL(**config['DB_CONFIG']))
    return engine

def init_db(config):
    envize_Session.configure(bind=_make_engine(config))