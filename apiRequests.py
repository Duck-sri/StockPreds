import os
import functools
from typing import Dict,List,Sequence,Union,Optional

import requests
import yaml
import json

import numpy as np
import pandas as pd
from datetime import datetime

def get_configs(fileName:str='./config.yaml') -> dict:
    with open(fileName,'r') as data:
        configs = yaml.load(data,Loader=yaml.CLoader)
    return configs


def get_ticker_history(symbol,config_file=None,out_folder='./data') -> Union[dict,None]:
    config = get_configs(config_file)  if (config_file is not None) else get_configs()
    outfile = os.path.join(out_folder,(symbol+'.json'))
    outfile = os.path.abspath(outfile)

    if (os.path.exists(outfile)):
        print('loaded')
        with open(outfile,'r') as file:
            data = json.load(file)
        return data

    site = config['SITE']
    query = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : symbol,
        "outputsize" : "full",
        "apikey" : config['APIKEY']
    }

    url = site + 'query?' + '&'.join([str(x)+'='+str(y) for x,y in query.items()])
    response = requests.get(url=url)
    if response:
        data = response.json()
        with open(outfile,'w') as out:
            json.dump(data,out)
        return response.json()
    else:
        return None


@functools.lru_cache(maxsize=10)
def symbol_to_dataframe(symbol:str) -> pd.DataFrame:
    json_out = get_ticker_history(symbol)
    daily_data = json_out['Time Series (Daily)']

    df = pd.DataFrame.from_dict(daily_data).transpose()
    df.columns = [col.split(' ')[-1] for col in list(df.columns)]
    to_datetime = lambda x : datetime.strptime(x ,"%Y-%m-%d")
    df['date'] = df.index.map(to_datetime)
    df['stock_id'] = df.index.map(lambda x: symbol)

    df['open'] = df['open'].astype(np.float32)
    df['high'] = df['high'].astype(np.float32)
    df['low'] = df['low'].astype(np.float32)
    df['close'] = df['close'].astype(np.float32)
    df['volume'] = df['volume'].astype(np.int32)

    return df
