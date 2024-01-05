import yfinance as yf
import pandas as pd
import time

# Set your stock and EMA parameters
stock_symbol = "AAPL"
short_ema_period = 12
long_ema_period = 26

# Paper trading account balance and stock count
account_balance = 10000  # Example starting balance
stock_count = 0

def fetch_stock_data(symbol, period="1d", interval="1m"):
    stock_data = yf.download(tickers=symbol, period=period, interval=interval)
    return stock_data

def calculate_ema(stock_data, period):
    return stock_data['Close'].ewm(span=period, adjust=False).mean()

def trading_strategy(data):
    buy_signal, sell_signal = False, False
    if data['ShortEMA'].iloc[-1] > data['LongEMA'].iloc[-1] and data['ShortEMA'].iloc[-2] < data['LongEMA'].iloc[-2]:
        buy_signal = True
    elif data['ShortEMA'].iloc[-1] < data['LongEMA'].iloc[-1] and data['ShortEMA'].iloc[-2] > data['LongEMA'].iloc[-2]:
        sell_signal = True
    return buy_signal, sell_signal

def simulate_buy(stock_price):
    global stock_count, account_balance
    if account_balance >= stock_price:
        account_balance -= stock_price
        stock_count += 1
        print(f"Bought 1 share at {stock_price}, new balance: {account_balance}")
    else:
        print("Insufficient balance to buy")

def simulate_sell(stock_price):
    global stock_count, account_balance
    if stock_count > 0:
        account_balance += stock_price
        stock_count -= 1
        print(f"Sold 1 share at {stock_price}, new balance: {account_balance}")
    else:
        print("No stock to sell")

# Main loop for live trading
while True:
    stock_data = fetch_stock_data(stock_symbol)
    stock_data['ShortEMA'] = calculate_ema(stock_data, short_ema_period)
    stock_data['LongEMA'] = calculate_ema(stock_data, long_ema_period)

    buy, sell = trading_strategy(stock_data)
    current_price = stock_data['Close'].iloc[-1]

    if buy:
        simulate_buy(current_price)
    elif sell:
        simulate_sell(current_price)

    print("running")
    time.sleep(1)  # Pause for 1 minute before next iteration