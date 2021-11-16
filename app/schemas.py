from typing import List,Dict,Tuple,Optional,Any

from pydantic import BaseModel,Json
import datetime

"""
OHLC
"""
class OHLCBase(BaseModel):
	id:int
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
	id:int
	date:datetime.date
	dividend:float

class DividendCreate(DividendBase):
	pass

class Dividends(DividendBase):

	class Config:
		orm_mode = True

"""
Stock Details
"""
class StockBase(BaseModel):
	name:str
	ticker:str
	sector:str


class StockCreate(StockBase):
	pass

class Stocks(StockBase):
	id:int
	daily_prices:List[OHLC] = list()
	dividends:List[Dividends] = list()

	class Config:
		orm_mode = True
