from typing import List,Union,Optional,Any

import yfinance as yf
import numpy as np
import pandas as pd

from sqlalchemy.orm import Session

import schemas
import crud
from database import engine

def addSymbol(db:Session,symbol:Union[str,List[str]],hist:bool=True):
    if (isinstance(symbol,list)):
        # TODO fix for multiple stocks
        data = yf.Ticker(*symbol)

    else:
        data = yf.Ticker(symbol)
        isin = data.isin
        ticker = data.ticker
        sector = data.info['sector']
        name = data.info['shortName']

        stock = schemas.StockCreate(
            isin = isin,
            name = name,
            ticker = ticker,
            sector = sector
        )
        crud.create_stock(db,stock)
        id = crud.get_stockid_from_isin(db,isin)
        if hist:
            df = data.history(period='max')
            df.drop(columns=['Dividends','Stock Splits'],inplace=True)
            df.reset_index(inplace=True)
            df.rename(lambda x:x.lower(),axis=1,inplace=True)
            df['id'] = df['date'].map(lambda x:id)
            df['date'] = df['date'].map(lambda x:x.date())
            df.set_index(['id','date'],inplace=True)
            df.to_sql(
                name='historical_prices',
                con=engine,
                if_exists='append',
                index_label=['id','date']
            )