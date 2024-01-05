import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate the RSI
def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = ((delta.where(delta > 0, 0)).rolling(window=window).mean())
    loss = ((-delta.where(delta < 0, 0)).rolling(window=window).mean())

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Load NVIDIA stock data
data = pd.read_csv('NVDA.csv')  
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Calculate RSI
data['RSI'] = compute_rsi(data)

# Define buy and sell conditions
overbought_threshold = 70
oversold_threshold = 30
data['Buy_Signal'] = (data['RSI'] < oversold_threshold) & (data['RSI'].shift(1) >= oversold_threshold)
data['Sell_Signal'] = (data['RSI'] > overbought_threshold) & (data['RSI'].shift(1) <= overbought_threshold)

# Plotting the price and RSI with buy/sell signals
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Plot stock close price
ax1.plot(data.index, data['Close'], label='Close Price')
ax1.set_title('NVIDIA Close Price and RSI Signals')
ax1.set_ylabel('Price')
ax1.grid(True)

# Plot RSI
ax2.plot(data.index, data['RSI'], label='RSI')
ax2.fill_between(data.index, overbought_threshold, oversold_threshold, color='lightcoral', alpha=0.5)
ax2.axhline(overbought_threshold, color='red', linestyle='--', linewidth=1.5, label='Overbought (70)')
ax2.axhline(oversold_threshold, color='green', linestyle='--', linewidth=1.5, label='Oversold (30)')
ax2.set_ylabel('RSI')
ax2.grid(True)

# Show buy/sell signals
ax1.plot(data[data['Buy_Signal']].index, data['Close'][data['Buy_Signal']], '^', markersize=10, color='g', lw=0, label='Buy Signal')
ax1.plot(data[data['Sell_Signal']].index, data['Close'][data['Sell_Signal']], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

# Show legend
ax1.legend()
ax2.legend()
plt.show()
