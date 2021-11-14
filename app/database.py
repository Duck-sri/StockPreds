import yaml

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from .models import *


# configs
# with open('./db.yml','r') as file:
#     database = yaml.load(file,Loader=yaml.Loader)

# db_uri = f"postgres+psycopg2://{database['user']}:{database['password']}@{database['host']}:{database['port']}/{database['name']}"
# engine = create_engine(db_uri)

db_uri = f"sqlite:///./stocks2.db"
engine = create_engine(db_uri,connect_args = {'check_same_thread':False}) # only needed for Sqlite
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# print(SessionLocal)
Base = declarative_base()