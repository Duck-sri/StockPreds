from typing import Any, List, Optional, Tuple, Union

import pandas as pd
import yfinance as yf

pd.options.mode.chained_assignment = None # for that annoying warning


import crud
import schemas
from datetime import datetime
from database import engine
from sqlalchemy.orm import Session
from tqdm.autonotebook import tqdm, trange

"""
This file contains utils for api requests done
"""

def ticker2Stock(ticker:yf.Ticker,isin:str)->Union[schemas.StockCreate,None]:
    # print(f"Downloading info for {ticker.ticker}...")
    if len(ticker.info) <= 3:
        print(f"Symbol : {ticker.ticker} doesn't exists")
        return None

    sector = ticker.info['sector']
    name = ticker.info['shortName']
    eps = ticker.info['trailingEps']
    pe = ticker.info['pegRatio']
    stock = schemas.StockCreate(
        isin = isin,
        name = name,
        id = ticker.ticker,
        sector = sector,
        eps = eps,
        pe = pe
    )
    return stock

def ticker2DividendDataframe(ticker:yf.Ticker,stock_id:int)->pd.DataFrame:
    df = ticker.dividends
    df = df.reset_index()
    df.rename(lambda x:x.lower(),axis=1,inplace=True)
    df.rename({'dividends':'dividend'},axis=1,inplace=True)
    df['id'] = df['date'].map(lambda _:stock_id)
    df['date'] = df['date'].map(lambda x:x.date())
    df.set_index(['id','date'],inplace=True)
    return df

def ticker2EarningDataframe(ticker:yf.Ticker,stock_id:int)->pd.DataFrame:
    df = ticker.earnings
    df = df.reset_index()
    df.rename(lambda x:x.lower(),axis=1,inplace=True)
    df.rename({'earnings':'earning'},axis=1,inplace=True)
    df['id'] = df['date'].map(lambda _:stock_id)
    df['date'] = df['date'].map(lambda x:datetime(year=x,day=1,month=1))
    df.set_index(['id','date'],inplace=True)
    return df

def processDataframe(df:pd.DataFrame,stock_id:int):
    if 'Dividends' in df.columns:
        df.drop(columns=['Dividends','Stock Splits'],inplace=True)
    df.reset_index(inplace=True)
    df.rename(lambda x:x.lower(),axis=1,inplace=True)
    df['id'] = df['date'].map(lambda _:stock_id)
    df['date'] = df['date'].map(lambda x:x.date())
    df.set_index(['id','date'],inplace=True)
    start = df.first_valid_index()
    df = df.loc[start:]
    df.dropna(inplace=True)
    return df

def ticker2Dataframe(ticker:yf.Ticker,stock_id:int)->pd.DataFrame:
    df = ticker.history(period='max')
    return processDataframe(df,stock_id)

def addSymbols(db:Session,symbols:List[Tuple[str,str]],hist:bool=True,div:bool=True,earning:bool=True)->List[schemas.Stocks]:
    # TODO fix for multiple stocks
    data = yf.Tickers(tickers=' '.join([x[0] for x in symbols]))
    isin_dict = {key:value for (key,value) in symbols}
    if hist:
        hist_data = yf.download(
            tickers=' '.join([x[0] for x in symbols]),
            period='max',
            group_by='ticker',
            auto_adjust=True,
            threads=True
        )
    total = len(symbols)
    done:int = 0
    got = []
    for sym,ticker in (t := tqdm(data.tickers.items())):
        stock = ticker2Stock(ticker,isin_dict[sym])
        if stock is not None:
            done += 1
            stock = crud.create_stock(db,stock)
            got.append(stock)
            print(f"Done adding {stock.name} in the Database")
            if hist:
                df = processDataframe(hist_data[sym],stock.id)
                crud.insertDataframe2sql(engine,df,'historical_prices')
                print(f"Done adding {stock.name} prices in the Database")
            if div:
                dividends = ticker2DividendDataframe(ticker,stock.id)
                crud.insertDataframe2sql(engine,dividends,'dividends')
                print(f"Done adding {stock.name} divs in the Database")
            if earning:
                earnings = ticker2EarningDataframe(ticker,stock.id)
                crud.insertDataframe2sql(engine,earnings,'earnings')
                print(f"Done adding {stock.name} earnings in the Database")

        t.set_description(f"{done}/{total} added!!")

    return got

def addSymbol(db:Session,symbol:Tuple[str,str],hist:bool=True,div:bool=True,earning:bool=True)->Union[schemas.Stocks,None]:
    ticker = yf.Ticker(symbol[0])
    stock = ticker2Stock(ticker,symbol[1])
    if stock is not None:
        stock = crud.create_stock(db,stock)
        print(f"Done adding {stock.name} in the Database")
        if hist:
            df = ticker2Dataframe(ticker,stock.id)
            crud.insertDataframe2sql(engine,df,'historical_prices')
            print(f"Done adding {stock.name} prices in the Database")
        if div:
            dividends = ticker2DividendDataframe(ticker,stock.id)
            crud.insertDataframe2sql(engine,dividends,'dividends')
            print(f"Done adding {stock.name} divs in the Database")
        if earning:
            earnings = ticker2EarningDataframe(ticker,stock.id)
            crud.insertDataframe2sql(engine,earnings,'earnings')
            print(f"Done adding {stock.name} earnings in the Database")

        print()

    return stock