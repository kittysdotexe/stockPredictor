import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load NVIDIA stock data
data = pd.read_csv('NVDA.csv')  # Replace with your file path
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Calculate EMA
short_window_ema = 12
long_window_ema = 26
data['Short_EMA'] = data['Close'].ewm(span=short_window_ema, adjust=False).mean()
data['Long_EMA'] = data['Close'].ewm(span=long_window_ema, adjust=False).mean()

# Calculate SMA
long_window_sma = 50
data['Long_SMA'] = data['Close'].rolling(window=long_window_sma).mean()

# Calculate RSI
window_length = 14
delta = data['Close'].diff(1)
delta = delta.dropna()
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0
roll_up = up.rolling(window_length).mean()
roll_down = down.abs().rolling(window_length).mean()
RS = roll_up / roll_down
data['RSI'] = 100.0 - (100.0 / (1.0 + RS))

# Define overbought and oversold levels
overbought_level = 70
oversold_level = 30

# Define buy and sell signals
data['Buy_Signal'] = ((data['RSI'] < oversold_level) & 
                      (data['Close'] > data['Short_EMA']) & 
                      (data['Close'] > data['Long_SMA']))

data['Sell_Signal'] = ((data['RSI'] > overbought_level) & 
                       (data['Close'] < data['Short_EMA']) & 
                       (data['Close'] < data['Long_SMA']))

# Plotting
plt.figure(figsize=(14,10))

# Plot Close Price, EMA, and SMA
plt.subplot(211)
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['Short_EMA'], label=f'{short_window_ema}-day EMA', color='red')
plt.plot(data['Long_SMA'], label=f'{long_window_sma}-day SMA', color='green')
plt.title('NVIDIA Close Price, EMA, SMA')
plt.legend()

# Plot RSI
plt.subplot(212)
plt.title('Relative Strength Index (RSI)')
plt.plot(data['RSI'], label='RSI', color='purple')
plt.axhline(overbought_level, color='red', linestyle='--')
plt.axhline(oversold_level, color='green', linestyle='--')
plt.fill_between(data.index, data['RSI'], overbought_level, where=(data['RSI'] >= overbought_level), color='red', alpha=0.5)
plt.fill_between(data.index, data['RSI'], oversold_level, where=(data['RSI'] <= oversold_level), color='green', alpha=0.5)
plt.legend()

# Show Buy/Sell Signals
plt.subplot(211)
plt.plot(data[data['Buy_Signal']].index, data['Close'][data['Buy_Signal']], '^', markersize=12, color='m', label='Buy Signal')
plt.plot(data[data['Sell_Signal']].index, data['Close'][data['Sell_Signal']], 'v', markersize=12, color='k', label='Sell Signal')
plt.legend()

plt.show()
