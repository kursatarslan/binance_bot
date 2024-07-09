# trade_bot.py

import pandas as pd
import numpy as np
import time
from binance_client import client

def calculate_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def trade_bot(symbol, quantity, rsi_buy_threshold=30, rsi_sell_threshold=70):
    while True:
        try:
            klines = client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1MINUTE, limit=100)
            data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                                 'close_time', 'quote_asset_volume', 'number_of_trades',
                                                 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            data['close'] = data['close'].astype(float)
            data['rsi'] = calculate_rsi(data)

            last_rsi = data['rsi'].iloc[-1]
            print(f"-->RSI: {last_rsi} symbol {symbol}")

            if last_rsi < rsi_buy_threshold:
                order = client.order_market_buy(symbol=symbol, quantity=quantity)
                print(f"Bought {quantity} {symbol} at market price. RSI: {last_rsi}")
                print(f"Order details: {order}")
            elif last_rsi > rsi_sell_threshold:
                order = client.order_market_sell(symbol=symbol, quantity=quantity)
                print(f"Sold {quantity} {symbol} at market price. RSI: {last_rsi}")
                print(f"Order details: {order}")

            time.sleep(30)
        except Exception as e:
            print(f"Error in trade_bot: {str(e)}")
            time.sleep(60)

def get_balance():
    try:
        balances = client.get_account()['balances']
        for balance in balances:
            asset = balance['asset']
            free = float(balance['free'])
            locked = float(balance['locked'])
            if free > 0 or locked > 0:
                print(f"{asset}: Free: {free}, Locked: {locked}")
    except Exception as e:
        print(f"Error in get_balance: {str(e)}")
