import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your historical stock price data
# Replace 'apple_stock_data.csv' and 'microsoft_stock_data.csv' with your actual file paths
apple_data = pd.read_csv('./Spreadsheets/AAPL.csv')
microsoft_data = pd.read_csv('./Spreadsheets/MSFT.csv')

# Make sure your date columns are in datetime format and set them as index
apple_data['Date'] = pd.to_datetime(apple_data['Date'])
microsoft_data['Date'] = pd.to_datetime(microsoft_data['Date'])

apple_data.set_index('Date', inplace=True)
microsoft_data.set_index('Date', inplace=True)

# Calculate daily returns
apple_data['Daily Return'] = apple_data['Close'].pct_change()
microsoft_data['Daily Return'] = microsoft_data['Close'].pct_change()

# Drop NA values
apple_data.dropna(inplace=True)
microsoft_data.dropna(inplace=True)

# Merge the datasets on Date
combined_data = pd.merge(apple_data['Daily Return'], microsoft_data['Daily Return'], left_index=True, right_index=True, how='inner')
combined_data.columns = ['Apple Daily Return', 'Microsoft Daily Return']

# Plotting the data
sns.jointplot(x='Apple Daily Return', y='Microsoft Daily Return', data=combined_data, kind='scatter', color='blue')

# Calculate and print the correlation coefficient
correlation = combined_data['Apple Daily Return'].corr(combined_data['Microsoft Daily Return'])
print(f'Correlation Coefficient: {correlation}')

plt.show()