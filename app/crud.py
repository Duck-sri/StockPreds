from sqlalchemy.orm import Session, session

import pandas as pd
import datetime
import yaml

import models,schemas

"""
This file contains all the crud operations done with the database and only the database
"""

# CREATE operations 

def create_stock(db:Session,stock:schemas.StockCreate):
	db_stock = models.Stocks(id=stock.id,isin=stock.isin,name=stock.name,pe=stock.pe,eps=stock.eps,sector=stock.sector)
	db.add(db_stock)
	db.commit()
	db.refresh(db_stock) # first deleted and got back from database
	return db_stock

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

def insertDataframe2sql(engine,df:pd.DataFrame,table_name:str):
		df.to_sql(
			# TODO add config file to change db name
				name=table_name,
				con=engine,
				if_exists='append',
				index_label=['id','date']
		)

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

def create_earning(db:Session,earning:schemas.EarningsCreate):
	db_earning = models.Dividends(
		id = earning.id,
		date = earning.date,
		earning = earning.earning
	)
	db.add(db_earning)
	db.commit()
	db.refresh(db_earning)
	return db_earning

# GET operations

def get_stock_by_ticker(db:Session,id:str):
	return db.query(models.Stocks).filter(models.Stocks.id == id).first()

def get_stocks(db:Session,skip:int=0,limit:int=100):
	return db.query(models.Stocks).offset(skip).limit(limit).all()

def get_stocks_by_sector(db:Session,sector:str):
	return db.query(models.Stocks).filter(models.Stocks.sector == sector).all()


def get_stock_prices(db:Session,stock_id:int,start:datetime.date=None,end:datetime.date=None):
	if(start or end):
		if (start is None):
			# end is there
			return db.query(models.OHLC).filter(models.OHLC.id == stock_id).filter(models.OHLC.date <= end).all()
		elif (end is None):
			# start is there
			return db.query(models.OHLC).filter(models.OHLC.id == stock_id).filter(models.OHLC.date >= start).all()
		else:
			return db.query(models.OHLC).filter(models.OHLC.id == stock_id).filter(models.OHLC.date.between(start,end)).all()
	else:
		return db.query(models.OHLC).filter(models.OHLC.id == stock_id).all()

def get_dividends_by_stock(db:Session,stock_id:int):
	return db.query(models.Dividends).filter(models.Dividends.id == stock_id).order_by(models.Dividends.date.desc()).all()
