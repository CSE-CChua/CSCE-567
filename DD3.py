import yfinance as yf
import pandas as pd

#Download NVDA data from Feb 1, 2019 to today
stock_df = yf.download('NVDA', start='2019-02-01')

#Drop unnecessary columns to keep only the relevant ones for our analysis
stock_df.columns = stock_df.columns.droplevel(1)

# Reset the index so 'Date' becomes a standard column we can merge on
stock_df.reset_index(inplace=True) 

# Ensure the 'Date' column in the stock data is properly formatted as a datetime object
stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.tz_localize(None)

# Load your manually created games dataset
games_df = pd.read_csv('games.csv')

# Ensure the 'Date' column in the games data is also formatted as a datetime object
games_df['Date'] = pd.to_datetime(games_df['Date'])

# Merge the datasets
# We use a 'left' merge to keep all the stock data days, while attaching 
# game titles to their specific release dates
merged_df = pd.merge(stock_df, games_df, on='Date', how='left')

# Calculate the 14-day and 30-day percentage changes
# .shift(-14) looks 14 rows (days) ahead to grab that future closing price
merged_df['14-Day % Change'] = (merged_df['Close'].shift(-14) - merged_df['Close']) / merged_df['Close']
merged_df['30-Day % Change'] = (merged_df['Close'].shift(-30) - merged_df['Close']) / merged_df['Close']

# Export the final cleaned dataset to a new CSV for Tableau
merged_df.to_csv('cleaned_hardware_games.csv', index=False)

print("Data merge complete. File saved as 'cleaned_hardware_games.csv'.")