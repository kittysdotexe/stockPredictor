import yfinance as yf
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data
def fetch_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    return stock_data['Close']  # Focusing on the closing prices

# Function to fetch Google Trends data
def fetch_trends_data(keyword, start_date, end_date):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=[keyword], timeframe=f'{start_date} {end_date}')
    trends_data = pytrends.interest_over_time()
    if not trends_data.empty:
        return trends_data[keyword]
    else:
        return None

# Example: Analyzing NVIDIA stock and the trend for the keyword 
stock_ticker = "NVDA"
keyword = "GPU"
start_date = "2020-01-01"
end_date = "2023-12-18"

# Fetching data
stock_data = fetch_stock_data(stock_ticker, start_date, end_date)
trends_data = fetch_trends_data(keyword, start_date, end_date)

# Normalizing data for comparison
if trends_data is not None and not stock_data.empty:
    stock_data_normalized = (stock_data - stock_data.min()) / (stock_data.max() - stock_data.min())
    trends_data_normalized = (trends_data - trends_data.min()) / (trends_data.max() - trends_data.min())

    #Exporting Data as CSV
    combined_data = pd.DataFrame({
        f'{stock_ticker}_Normalized_Stock': stock_data_normalized,
        f'{keyword}_Normalized_Trends': trends_data_normalized
    })
    combined_data.to_csv('normalized_data.csv')

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data_normalized, label=f'{stock_ticker} Stock Price')
    plt.plot(trends_data_normalized, label=f'Google Trends for "{keyword}"')
    plt.title(f'{stock_ticker} Stock Price vs Google Trends for "{keyword}"')
    plt.xlabel('Date')
    plt.ylabel('Normalized Values')
    plt.legend()
    plt.show()
else:
    print("No data available for the given dates or keywords.")
