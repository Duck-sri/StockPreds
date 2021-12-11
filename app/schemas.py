import datetime
from typing import Union

from pydantic import BaseModel, Json

"""
OHLC
"""
class OHLCBase(BaseModel):
	id:str
	date:datetime.date
	open_:float
	high:float
	low:float
	close:float
	volume:int

class OHLCCreate(OHLCBase):
	pass

class OHLC(OHLCBase):

	class Config:
		orm_mode = True

"""
Dividends
"""

class DividendBase(BaseModel):
	id:str
	date:datetime.date
	dividend:float

class DividendCreate(DividendBase):
	pass

class Dividends(DividendBase):

	class Config:
		orm_mode = True

class EarningsBase(BaseModel):
	id:str
	date:datetime.date
	earning:float

class EarningsCreate(EarningsBase):
	pass

class Earnings(EarningsBase):

	class Config:
		orm_mode = True

"""
Stock Details
"""
class StockBase(BaseModel):
	isin:str
	name:str
	id:str
	sector:str


class StockCreate(StockBase):
	eps:Union[None,float]
	pe:Union[None,float]

class Stocks(StockBase):
	# daily_prices:List[OHLC] = list()
	# dividends:List[Dividends] = list()
	# earnings:List[Earnings] = list()

	class Config:
		orm_mode = True