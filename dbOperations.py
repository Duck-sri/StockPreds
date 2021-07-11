import os

import yaml

from apiRequests import symbol_to_dataframe,get_configs

from sqlalchemy import create_engine
from sqlalchemy import Table,Column,Date,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

def write_symbols_to_db(symbols:List[str],engine):
    for symbol in symbols:
        df = symbol_to_dataframe(symbol)
        try:
            df.to_sql('prices',engine,if_exists='append',index=False)
        except IntegrityError:
            print(f"Already a key exsists in date for Ticker: {symbol}")

# configs
def main():
    with open('db.yml','r') as file:
        database = yaml.load(file,Loader=yaml.CLoader)

    db_uri = f"postgres+psycopg2://{database['user']}:{database['password']}@{database['host']}:{database['port']}/{database['name']}"
    engine = create_engine(db_uri)
    print(engine)

    tickers = get_configs('./config.yaml')['tickers']

    write_symbols_to_db(tickers,engine)
    print("Done Writing data to database")

if __name__ == '__main__':
    main()