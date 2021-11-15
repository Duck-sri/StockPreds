from pydantic.main import validate_model
from pydantic.types import SecretBytes
import sqlalchemy
from sqlalchemy.orm import Session, session

import pandas as pd

import datetime

from sqlalchemy.sql.functions import mode

import models,schemas


def create_stock(db:Session,stock:schemas.StockCreate):
	db_stock = models.Stocks(name=stock.name,ticker=stock.ticker,sector=stock.sector)
	db.add(db_stock)
	db.commit()
	db.refresh(db_stock) # first deleted and got back from database
	return db_stock

def get_stock_by_id(db:Session,stock_id:int):
	return db.query(models.Stocks).filter(models.Stocks.id == stock_id).first()

def get_stocks(db:Session,skip:int=0,limit:int=100):
	return db.query(models.Stocks).offset(skip).limit(limit).all()

def get_stocks_by_sector(db:Session,sector:str):
# TODO a way to select stocks by sectors
	...

def create_daily_price(db:Session,price:schemas.OHLCCreate):
	db_price = models.OHLC(
		id = price.id,
		date = price.date,
		open_ = price.open_,
		high = price.high,
		low = price.low,
		close = price.close,
		volume = price.volume
	)
	db.add(db_price)
	db.commit()
	db.refresh(db_price)
	return db_price

def insertDataframe2sql(engine:sqlalchemy.engine.base.Engine,df:pd.DataFrame,table_name:str):
		df.to_sql(
			# TODO add config file to change db name
				name=table_name,
				con=engine,
				if_exists='append',
				index_label=['id','date']
		)

def get_stock_prices(db:Session,stock_id:int,start:datetime.date=None,end:datetime.date=None):
	qr_symbol = db.query(models.OHLC).filter(models.OHLC.id == stock_id)
	if(start or end):
		if (start is None):
			# end is there
			return qr_symbol.filter(models.OHLC.date <= end).all()
		elif (end is None):
			# start is there
			return qr_symbol.filter(models.OHLC.date >= start).all()
		else:
			return qr_symbol.filter(models.OHLC.date.between(start,end)).all()
	else:
		return qr_symbol.all()


def create_dividend(db:Session,div:schemas.DividendCreate):
	db_div = models.Dividends(
		id = div.id,
		date = div.date,
		dividend = div.dividend
	)
	db.add(db_div)
	db.commit()
	db.refresh(db_div)
	return db_div

def get_dividends_by_stock(db:Session,stock_id:int):
	return db.query(models.Dividends).filter(models.Dividends.id == stock_id).order_by(models.Dividends.date.desc()).all()