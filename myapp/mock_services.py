import pandas as pd
from binance.client import Client
from .utils import *
import random


available_coins = [
    "ALPHA", "APE", "ARK", "AXS", "BIGTIME", "BLUR", "COMBO", "DYDX", "FET", "FRONT",
    "GALA", "GMT", "GRT", "HFT", "IDEX", "IMX", "INJ", "KNC", "MAGIC", "MBL", "NTRN",
    "OCEAN", "PEOPLE", "PERP", "REEF", "SKL", "STORJ", "SUI", "TIA", "XVG", "ZRX",
    "ALPHA", "APE", "ARK", "AXS", "BIGTIME", "BLUR", "COMBO", "DYDX", "FET", "FRONT",
    "GALA", "GMT", "GRT", "HFT", "IDEX", "IMX", "INJ", "KNC", "MAGIC", "MBL", "NTRN",
    "OCEAN", "PEOPLE", "PERP", "REEF", "SKL", "STORJ", "SUI", "TIA", "XVG", "ZRX",
    "ALPHA", "APE", "ARK", "AXS", "BIGTIME", "BLUR", "COMBO", "DYDX", "FET", "FRONT",
    "GALA", "GMT", "GRT", "HFT", "IDEX", "IMX", "INJ", "MAGIC", "MBL", "NTRN", "OCEAN",
    "PEOPLE", "PERP", "REEF", "SKL", "STORJ", "SUI", "TIA", "XVG", "ZRX", "ALPHA", "APE",
    "ARK", "AXS", "BIGTIME", "BLUR", "COMBO", "DYDX", "FET", "FRONT", "GALA", "GMT",
    "GRT", "HFT", "IDEX", "IMX", "INJ", "MAGIC", "MBL", "NTRN", "OCEAN", "PEOPLE",
    "PERP", "REEF", "SKL", "STORJ", "SUI", "TIA", "TRU", "XVG", "ZRX", "ALPHA", "APE",
    "ARK", "AXS", "BIGTIME", "BLUR", "COMBO", "FRONT", "GALA", "GMT", "GRT", "HFT",
    "IDEX", "IMX", "INJ", "MAGIC", "MBL", "NTRN", "OCEAN", "PEOPLE", "REEF", "SKL",
    "STORJ", "TIA", "TRU", "XVG", "ALPHA", "APE", "ARK", "AXS", "BIGTIME", "BLUR",
    "FRONT", "GALA", "GMT", "GRT", "HFT", "IDEX", "IMX", "INJ", "MAGIC", "REEF",
    "SKL", "STORJ", "TRU", "XVG", "ALPHA", "APE", "ARK", "AXS", "BIGTIME", "FRONT",
    "GALA", "GMT", "GRT", "IDEX", "IMX", "INJ", "MAGIC", "RUNE", "SKL", "STORJ", "TRU", "XVG"
]



def fetch_mock_account_history(api_key, secret_key):
    mock_data = []
    # Generate data for the last 33 days
    for i in range(33):
        # Calculate the date for each day
        day_date = datetime.utcnow() - timedelta(days=i)
        day_timestamp = int(day_date.timestamp() * 1000)

        # Generate 33 records per day
        for j in range(33):
            record = {
                "buyer": random.choice([True, False]),
                "commission": f"{random.uniform(0.0, 1.0):.8f}",
                "commissionAsset": "USDT",
                "day": day_date.day,
                "id": random.randint(50000000, 60000000),
                "maker": random.choice([True, False]),
                "marginAsset": "USDT",
                "orderId": random.randint(10000000000, 99999999999),
                "positionSide": random.choice(["LONG", "SHORT"]),
                "price": f"{random.uniform(0.1, 300.0):.5f}",
                "qty": random.randint(1, 10000),
                "quoteQty": f"{random.uniform(10.0, 1000.0):.7f}",
                "realizedPnl": f"{random.uniform(-10.0, 10.0):.8f}",
                "side": random.choice(["BUY", "SELL"]),
                "symbol": random.choice(available_coins) + "USDT",
                "time": day_timestamp,
                "utc_time": day_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            mock_data.append(record)

def fetch_mock_open_positions(api_key,secret_key):
    client = Client(api_key, secret_key)
    positions = [{
        "symbol": "BTCUSDT",
        "positionAmt": "0.1",
        "entryPrice": "22185.2",
        "breakEvenPrice": "0.0",  
        "markPrice": "21123.05052574",
        "unRealizedProfit": "-1.06214947",
        "liquidationPrice": "19731.45529116",
        "leverage": "4",
        "maxNotionalValue": "100000000",
        "marginType": "cross",
        "isolatedMargin": "0.00000000",
        "isAutoAddMargin": "false",
        "positionSide": "LONG",
        "notional": "21.12305052",
        "isolatedWallet": "0",
        "updateTime": 1655217461579
    }]

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


def fetch_mock_income_history(api_key, secret_key):
    base_date = datetime.utcnow()
    income_history = []

    for i in range(30):
        date = base_date - timedelta(days=i)
        base_timestamp = int(date.timestamp() * 1000)
        accumulated_minutes = 0

        num_trades = random.randint(1, 5)
        for j in range(num_trades):
            # Increment time in minutes for each trade
            accumulated_minutes += random.randint(1, 60)
            trade_timestamp = base_timestamp + accumulated_minutes * 60000

            # Randomly decide if this trade is a funding fee (5% chance)
            if random.random() < 0.05:
                income_type = "FUNDING_FEE"
            else:
                income_type = "REALIZED_PNL"

            symbol = random.choice(available_coins)+"USDT"
            # Add the trade record
            trade_record = {
                "asset": "USDT",
                "income": f"{random.uniform(-100.0, 100.0):.8f}",
                "incomeType": income_type,
                "info": str(random.randint(1000000, 9999999)),
                "symbol": symbol,
                "time": trade_timestamp,
                "tradeId": str(random.randint(1000000, 9999999)),
                "tranId": random.randint(1000000000000, 9999999999999),
            }
            income_history.append(trade_record)

            # If the trade was REALIZED_PNL, add a corresponding COMMISSION trade
            if income_type == "REALIZED_PNL":
                accumulated_minutes += random.randint(1, 60)  # Increment time
                trade_timestamp = base_timestamp + accumulated_minutes * 60000

                commission_record = {
                    "asset": "USDT",
                    "income": f"{random.uniform(-10.0, -1.0):.8f}",
                    "incomeType": "COMMISSION",
                    "info": str(random.randint(1000000, 9999999)),
                    "symbol": symbol,
                    "time": trade_timestamp,
                    "tradeId": str(random.randint(1000000, 9999999)),
                    "tranId": random.randint(1000000000000, 9999999999999),
                }
                income_history.append(commission_record)


                if income_type == "FUNDING_FEE":

                    commission_record = {
                        "asset": "USDT",
                        "income": f"{random.uniform(-10.0, 10.0):.8f}",
                        "incomeType": "FUNDING_FEE",
                        "info": str(random.randint(1000000, 9999999)),
                        "symbol": symbol,
                        "time": trade_timestamp,
                        "tradeId": str(random.randint(1000000, 9999999)),
                        "tranId": random.randint(1000000000000, 9999999999999),
                    }
                    income_history.append(commission_record)


    df_income = pd.DataFrame(income_history)
    df_income['utc_time'] = df_income['time'].apply(convert_timestamp_to_utc)
    df_income['day'] = df_income['utc_time'].dt.day

    
    return df_income


def fetch_mock_balance():
    return random.randint(500,2500)
