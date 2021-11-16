from typing import List,Optional,Any,Union
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

import datetime

from sqlalchemy.sql.roles import LimitOffsetRole
from starlette.responses import HTMLResponse, JSONResponse

from app.database import SessionLocal
from app import apiRequests, models,schemas,crud

app = FastAPI()

def get_db():
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()

# TODO add if ticker/id exists func

@app.get(path='/stocks/',response_model=List[schemas.Stocks])
def get_stocks(skip:int=0,limit:int=100,db:Session= Depends(get_db)):
  return crud.get_stocks(db,skip,limit)

@app.get(path='/stocks/{ticker}',response_model=schemas.Stocks)
def get_stock(ticker:str,db:Session= Depends(get_db)):
	res =  crud.get_stock_by_id(db,int(ticker)) if ticker.isnumeric() else crud.get_stock_by_ticker(db,ticker)
	return res if res else JSONResponse({"message":f"Stock id(or)ticker : {ticker} does not exists in database"})

@app.get(path='/history/{ticker}',response_model=List[schemas.OHLC])
def get_history(ticker:str,start:datetime.date=None,end:datetime.date=None,db:Session=Depends(get_db)):
	# TODO add way to mention dates in query headers
	stock_id:int = int(ticker) if ticker.isnumeric() else crud.get_stock_by_ticker(db,ticker).id
	return crud.get_stock_prices(db,stock_id,start=start,end=end)

@app.get(path='/dividends/{ticker}',response_model=List[schemas.Dividends])
def get_dividends(ticker:str,db:Session=Depends(get_db)):
	if ticker.isnumeric():
		stock_id = int(ticker)
	else:
		stock = crud.get_stock_by_ticker(db,ticker)
		if (stock is not None): stock_id = stock.id
		else: return JSONResponse({"message" : f"Stock id(or)ticker : {ticker} does not exists in database"})
	return crud.get_dividends_by_stock(db,stock_id)
	

@app.post(path='/add/{ticker}',response_model=Union[None,schemas.Stocks])
def add_stock(ticker:str,db:Session = Depends(get_db)):
	if get_stock(ticker,db) is not None:
		return JSONResponse({ "message" : f"{ticker} already exists"})
	else:
		return apiRequests.addSymbol(db,ticker)