from sqlalchemy.ext.declarative import declarative_base 

from sqlalchemy import Column,ForeignKey
from sqlalchemy.sql.sqltypes import String,Date,REAL,VARCHAR,Boolean,Integer,Text
from sqlalchemy.orm import relationship

from database import Base


class Stocks(Base):
	__tablename__:str = 'stocks'

	id = Column(Integer,name='id',primary_key=True)
	isin = Column(String,name='isin',nullable=False,unique=True)
	name = Column(String,name='stock_name',nullable=False)
	ticker = Column(String,name='ticker',nullable=False)
	# TODO find a way to have a master sector table
	sector = Column(Text,name='sector',nullable=True)

	historical_prices = relationship("OHLC",back_populates='stocks')
	dividends = relationship("Dividends",back_populates='stocks')

	def __repr__(self):
		return f"{self.ticker} : ({self.isin})\nName: {self.name}\nSector : {self.sector}"

class OHLC(Base):
	__tablename__:str = 'historical_prices'

	id = Column(Integer,ForeignKey("stocks.id"),name='id',primary_key=True)
	date = Column(Date,name='date',primary_key=True,index=True)
	open_ = Column(REAL,name='open',nullable=False)
	high = Column(REAL,name='high',nullable=False)
	low = Column(REAL,name='low',nullable=False)
	close = Column(REAL,name='close',nullable=False)
	volume = Column(Integer,name='volume',nullable=False)

	stocks = relationship("Stocks",back_populates='historical_prices')


class Dividends(Base):
	__tablename__:str = 'dividends'

	id = Column(Integer,ForeignKey("stocks.id"),name='id',primary_key=True)
	date = Column(Date,name='date',primary_key=True)
	dividend = Column(REAL,name='dividend')

	stocks = relationship('Stocks',back_populates='dividends')