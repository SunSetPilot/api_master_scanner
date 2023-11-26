from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import config.settings

Base = declarative_base()

engine = create_engine(config.settings.mysql_dsn, pool_size=20, max_overflow=0, pool_pre_ping=True)


def get_db_session():
    return sessionmaker(bind=engine)()

