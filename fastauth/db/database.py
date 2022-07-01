from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.environ.get('DB_CREDS')

engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
