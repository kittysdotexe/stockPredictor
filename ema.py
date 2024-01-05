import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load stock data
data = pd.read_csv('NVDA.csv')  # Replace with your file path
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Calculate EMAs
short_window = 12  # Short-term EMA window (e.g., 12 days)
long_window = 26  # Long-term EMA window (e.g., 26 days)
data['Short_EMA'] = data['Close'].ewm(span=short_window, adjust=False).mean()
data['Long_EMA'] = data['Close'].ewm(span=long_window, adjust=False).mean()

# Generate signals
data['Signal'] = 0
data['Signal'] = np.where(data['Short_EMA'] > data['Long_EMA'], 1, 0)
data['Position'] = data['Signal'].diff()

# Plotting
plt.figure(figsize=(10,6))
plt.grid(True)
plt.plot(data['Close'], label='NVIDIA Close Price')
plt.plot(data['Short_EMA'], label=f'{short_window}-day EMA')
plt.plot(data['Long_EMA'], label=f'{long_window}-day EMA')
plt.plot(data['Position'], label='Buy/Sell Signal', linestyle='--')
plt.title('NVIDIA Stock Price and EMA Crossover Strategy')
plt.legend()
plt.show()
