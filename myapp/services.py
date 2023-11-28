import pandas as pd
from binance.client import Client
from .utils import *


def fetch_income_history(api_key, secret_key):
    client = Client(api_key, secret_key)
    income_history = client.futures_income_history(limit=1000)

    df_income = pd.DataFrame(income_history)
    df_income['utc_time'] = df_income['time'].apply(convert_timestamp_to_utc)
    df_income['day'] = df_income['utc_time'].dt.day

    
    return df_income


def fetch_account_history(api_key, secret_key):
    client = Client(api_key, secret_key)
    account_history = client.futures_account_trades(limit=1000)

    account_history = pd.DataFrame(account_history)
    account_history['utc_time'] = account_history['time'].apply(convert_timestamp_to_utc)
    account_history['day'] = account_history['utc_time'].dt.day

    
    return account_history


def get_position_from_account(account_history):
    df = pd.DataFrame(account_history)
    df['utc_time'] = df['time'].apply(convert_timestamp_to_utc)
    df['date'] = df['utc_time'].dt.day
    df['minute'] = df['utc_time'].dt.minute
    df['realizedPnl'] = df['realizedPnl'].astype(float)

    aggregations = {
    'symbol': lambda x: x.mode().iloc[0] if x.value_counts().iloc[0] > 1 else x.iloc[0],
    'realizedPnl': 'sum', 
    'utc_time': lambda x: mode(x).mode[0],
    'date' : lambda x: mode(x).mode[0],
    'minute' : lambda x: mode(x).mode[0],
    'positionSide' : lambda x: x.mode().iloc[0] if x.value_counts().iloc[0] > 1 else x.iloc[0],
    'maker' : lambda x: x.mode().iloc[0] if x.value_counts().iloc[0] > 1 else x.iloc[0],
}
    
    PNL = df.groupby('orderId').agg(aggregations).reset_index()
    PNL = PNL.sort_values(by = 'utc_time').reset_index(drop=True)

    PNL['utc_time'] = PNL['utc_time'].shift(1)
    PNL = PNL[PNL['realizedPnl']!=0]

    PNL.fillna(pd.Timestamp('2023-01-01'), inplace=True)

    return PNL


def fetch_balance(api_key,secret_key):
    client = Client(api_key, secret_key)
    balance = client.futures_account_balance()
    current_balance = balance[5]['crossWalletBalance']
    return current_balance

def fetch_open_orders(api_key,secret_key):
    client = Client(api_key, secret_key)
    open_orders = client.futures_get_open_orders()
    if len(open_orders) > 0:
        open_orders_df = pd.DataFrame(open_orders)[['symbol','price','origQty','side','positionSide','time']]
        open_orders_df['utc_time'] = open_orders_df['time'].apply(convert_timestamp_to_utc)
    else:
        print('No open orders')
        open_orders_df = pd.DataFrame(columns = ['symbol','price','origQty','side','positionSide','time'])
    return open_orders_df


def fetch_open_positions(api_key,secret_key):
    client = Client(api_key, secret_key)
    positions = client.futures_position_information()
    columns = ['symbol','entryPrice','breakEvenPrice','unRealizedProfit','liquidationPrice','leverage','notional',
                        'positionSide']
    open_position_df  = pd.DataFrame(columns = columns)
    open_position = []
    for position in positions:
        if float(position['positionAmt']) != 0:  # Filters out positions that are not open (position amount is not zero)
            open_position.append(position)
    if open_position is not None:
        open_position_df = pd.DataFrame(open_position,columns = columns)
        
    return open_position_df







