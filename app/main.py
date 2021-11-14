from typing import List

from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session

import crud,models,schemas
from database import SessionLocal,engine

# Creating all the tables
models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # dependency
# def get_db():
# 	# this will close once the dbsession is over by itself!!
# 	db = SessionLocal()
# 	try:
# 		yield db
# 	finally:
# 		db.close()
