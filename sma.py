import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load stock data
data = pd.read_csv('NVDA.csv')  
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Calculate SMAs
short_window = 20  # Short-term SMA window (e.g., 40 days)
long_window = 100  # Long-term SMA window (e.g., 100 days)
data['Short_SMA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['Long_SMA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Generate signals
data['Signal'] = 0
data['Signal'][short_window:] = np.where(data['Short_SMA'][short_window:] > data['Long_SMA'][short_window:], 1, 0)
data['Position'] = data['Signal'].diff()

# Plotting
plt.figure(figsize=(10,6))
plt.grid(True)
plt.plot(data['Close'], label='NVDA Close Price')
plt.plot(data['Short_SMA'], label='20-day SMA')
plt.plot(data['Long_SMA'], label='100-day SMA')
plt.plot(data['Position'], label='Buy/Sell Signal', linestyle='--')
plt.title('NVDA Stock Price and SMA Crossover Strategy')
plt.legend()
plt.show()