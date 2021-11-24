from re import S
from typing import List,Union,Optional,Any
from sqlalchemy.sql.base import SchemaEventTarget
from sqlalchemy.util.langhelpers import symbol

import yfinance as yf
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None # for that annoying warning

import json

from sqlalchemy.orm import Session

from tqdm import tqdm,trange

import schemas,crud
from database import engine

def ticker2Stock(ticker:yf.Ticker)->schemas.StockCreate:
    # print(f"Downloading info for {ticker.ticker}...")
    if len(ticker.info) <= 3:
        print(f"Symbol : {ticker.ticker} doesn't exists")
        return None

    sector = ticker.info['sector']
    name = ticker.info['shortName']
    stock = schemas.StockCreate(
        name = name,
        ticker = ticker.ticker,
        sector = sector
    )
    return stock

def ticker2DividendDataframe(ticker:yf.Ticker,stock_id:int)->pd.DataFrame:
    df = ticker.dividends
    df = df.reset_index()
    df.rename(lambda x:x.lower(),axis=1,inplace=True)
    df.rename({'dividends':'dividend'},axis=1,inplace=True)
    df['id'] = df['date'].map(lambda x:stock_id)
    df['date'] = df['date'].map(lambda x:x.date())
    df.set_index(['id','date'],inplace=True)
    return df

def processDataframe(df:pd.DataFrame,stock_id:int):
    if 'Dividends' in df.columns:
        df.drop(columns=['Dividends','Stock Splits'],inplace=True)
    df.reset_index(inplace=True)
    df.rename(lambda x:x.lower(),axis=1,inplace=True)
    df['id'] = df['date'].map(lambda x:stock_id)
    df['date'] = df['date'].map(lambda x:x.date())
    df.set_index(['id','date'],inplace=True)
    start = df.first_valid_index()
    df = df.loc[start:]
    df.dropna(inplace=True)
    return df

def ticker2Dataframe(ticker:yf.Ticker,stock_id:int)->pd.DataFrame:
    df = ticker.history(period='max')
    return processDataframe(df,stock_id)

def addSymbols(db:Session,symbols:List[str],hist:bool=True,div:bool=True)->List[schemas.Stocks]:
    # TODO fix for multiple stocks
    data = yf.Tickers(tickers=' '.join(symbols))
    if hist:
        hist_data = yf.download(
            tickers=' '.join(symbols),
            period='max',
            group_by='ticker',
            auto_adjust=True,
            threads=True
        )
    total = len(symbols)
    done:int = 0
    got = []
    for sym,ticker in (t := tqdm(data.tickers.items())):
        stock = ticker2Stock(ticker)
        if stock is not None:
            done += 1
            stock = crud.create_stock(db,stock)
            got.append(stock)
            t.set_description(f"Done adding {stock.name} in the Database")
            if hist:
                df = processDataframe(hist_data[sym],stock.id)
                crud.insertDataframe2sql(engine,df,'historical_prices')
                t.set_description(f"Done adding {stock.name} prices in the Database")
            if div:
                dividends = ticker2DividendDataframe(ticker,stock.id)
                crud.insertDataframe2sql(engine,dividends,'dividends')
                t.set_description(f"Done adding {stock.name} divs in the Database")

        t.set_description(f"{done}/{total} added!!")

    return got

def addSymbol(db:Session,symbol:str,hist:bool=True,div:bool=True)->schemas.Stocks:
    ticker = yf.Ticker(symbol)
    stock = ticker2Stock(ticker)
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

        print()

    return stock
