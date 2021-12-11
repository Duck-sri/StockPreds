from database import Base
from pydantic.types import Json
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import (JSON, VARCHAR, Boolean, Date, Integer,
                                     Numeric, Text)

# TODO add model for ticker

class Stocks(Base):
	__tablename__:str = 'stocks'

	id = Column(VARCHAR,name='id',primary_key=True) # ticker
	isin = Column(VARCHAR,name='isin',nullable=False,unique=True)
	name = Column(Text,name='stock_name',nullable=False)
	# TODO find a way to have a master sector table
	eps = Column(Numeric,name='EPS',nullable=True)
	pe = Column(Numeric,name='P/E',nullable=True)
	sector = Column(Text,name='sector',nullable=True)

	historical_prices = relationship("OHLC",back_populates='stock')
	dividends = relationship("Dividends",back_populates='stock')
	earnings = relationship("Earnings",back_populates='stock')

	def __repr__(self):
		return f"{self.ticker}\nName: {self.name}\nSector : {self.sector}"

class OHLC(Base):
	__tablename__:str = 'historical_prices'

	id = Column(VARCHAR,ForeignKey("stocks.id"),name='id',primary_key=True)
	date = Column(Date,name='date',primary_key=True,index=True)
	open_ = Column(Numeric,name='open',nullable=False)
	high = Column(Numeric,name='high',nullable=False)
	low = Column(Numeric,name='low',nullable=False)
	close = Column(Numeric,name='close',nullable=False)
	volume = Column(Integer,name='volume',nullable=False)

	stock = relationship("Stocks",back_populates='historical_prices')


class Dividends(Base):
	__tablename__:str = 'dividends'

	id = Column(VARCHAR,ForeignKey("stocks.id"),name='id',primary_key=True)
	date = Column(Date,name='date',primary_key=True)
	dividend = Column(Numeric,name='dividend')

	stock = relationship('Stocks',back_populates='dividends')

class Earnings(Base):
	__tablename__:str = 'earnings'

	id = Column(VARCHAR,ForeignKey("stocks.id"),name='id',primary_key=True)
	date = Column(Date,name='date',primary_key=True)
	earning = Column(Numeric,name='earning')

	stock = relationship('Stocks',back_populates='earnings')