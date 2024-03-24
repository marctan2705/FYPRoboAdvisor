import pandas as pd
import yfinance as yf
import statsmodels.api as sm

# Read the Fama-French factors from a CSV file
ff_factors = pd.read_csv('ff_data.csv', skiprows=2, index_col=0)

# Convert the index to datetime
ff_factors.index = pd.to_datetime(ff_factors.index, format='%Y%m')

# Fetch stock returns using yfinance
stock_symbol = 'AAPL'  # Replace with the stock symbol you're analyzing
start_date = '1926-07-01'  # Adjust the start date as needed
end_date = '1927-01-01'  # Adjust the end date as needed

# Fetching data
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate daily returns
stock_data['Return'] = stock_data['Adj Close'].pct_change()

# Convert the index to a column and filter the required columns
stock_returns = stock_data.reset_index()[['Date', 'Return']]
stock_returns.rename(columns={'Date': 'date', 'Return': 'stock_return'}, inplace=True)

# Ensure the date formats match and merge the datasets on the date
# Note: You might need to adjust the merging process depending on the frequency of your data
ff_factors.reset_index(inplace=True)
ff_factors.rename(columns={'index': 'date'}, inplace=True)
ff_factors['date'] = ff_factors['date'].dt.to_period('M').dt.to_timestamp('M')

data = pd.merge(stock_returns, ff_factors, how='inner', left_on='date', right_on='date')

# Calculate excess returns for the stock by subtracting the Risk-Free rate
data['excess_return'] = data['stock_return'] - data['RF']

# Independent variables (Fama-French factors)
X = data[['Mkt-RF', 'SMB', 'HML']]

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Dependent variable (excess returns of the stock)
y = data['excess_return']

# Perform the regression
model = sm.OLS(y, X).fit()

# Print out the results
print(model.summary())
