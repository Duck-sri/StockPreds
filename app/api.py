import datetime
from typing import Any, List, Optional, Union

import apiRequests
import crud
import pandas as pd
import schemas
import yaml
from database import SessionLocal
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm.session import Session

app = FastAPI()

with open('./db.yml','r') as configFile:
  cnf = yaml.load(configFile,Loader=yaml.Loader)

nse_symbols = pd.read_csv(cnf['symbols_file'],index_col='SYMBOL')
nse_symbols.index = nse_symbols.index.map(lambda x:x+'.NS')

def get_db():
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()

# GET requests

@app.get(path='/stocks/',response_model=List[schemas.Stocks])
def get_stocks(skip:int=0,limit:int=100,db:Session= Depends(get_db)):
  return crud.get_stocks(db,skip,limit)

@app.get(path='/stock/{ticker}',response_model=schemas.Stocks)
def get_stock(ticker:str,db:Session= Depends(get_db)):
	res =  crud.get_stock_by_id(db,ticker) if ticker.isnumeric() else crud.get_stock_by_ticker(db,ticker)
	return res if res else JSONResponse({"message":f"Stock id(or)ticker : {ticker} does not exists in database"})

@app.get(path='/history/{ticker}',response_model=List[schemas.OHLC])
def get_history(ticker:str,start:datetime.date=None,end:datetime.date=None,db:Session=Depends(get_db)):
	# TODO add way to mention dates in query headers
	stock = crud.get_stock_by_ticker(db,ticker)
	if stock is not None:
		stock_id = stock.id
		return crud.get_stock_prices(db,stock_id,start=start,end=end)
	else:
		return JSONResponse({"message" : f"{ticker} does not exsist in database"})

@app.get(path='/dividends/{ticker}',response_model=List[schemas.Dividends])
def get_dividends(ticker:str,db:Session=Depends(get_db)):
	stock = crud.get_stock_by_ticker(db,ticker)
	if (stock is not None): stock_id = stock.id
	else: return JSONResponse({"message" : f"{ticker} does not exists in database"})
	return crud.get_dividends_by_stock(db,stock_id)

# POST requests

@app.post(path='/add/{ticker}',response_model=Union[None,schemas.Stocks])
def add_stock(ticker:str,db:Session = Depends(get_db)):
	got = crud.get_stock_by_ticker(db,ticker)
	if isinstance(got,JSONResponse):
		return {"message" : f"{ticker} already exists"} + got
	else:
		try:
			isin = nse_symbols[' ISIN NUMBER'].loc[ticker]
			return apiRequests.addSymbol(db,(ticker,isin))
		except KeyError:
			return JSONResponse({"message" : f"{ticker} does exists in NSE"})