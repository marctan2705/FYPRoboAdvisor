import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from datetime import datetime
def fetch_risk_free_rate():
    # The ticker for 3-month Treasury Bill is often used as a proxy for the risk-free rate
    t_bill_ticker = '^IRX'
    
    # Fetch the latest data
    t_bill = yf.Ticker(t_bill_ticker)
    
    # Get the latest closing price, which represents the annualized yield in percentage
    # Note: This might need adjustments based on the exact data structure and availability
    hist = t_bill.history(period="1d")
    latest_yield = hist['Close'].iloc[-1]

    # Convert the yield to a decimal for use in calculations (e.g., 0.025 for 2.5%)
    risk_free_rate = latest_yield / 100

    return risk_free_rate

# Define stock symbols
stocks = ['AAPL', 'MSFT']  # Example stocks, adjust as needed

# Download historical data
data = yf.download(stocks, start='2023-01-01', end='2023-12-31')['Adj Close']

# Calculate daily returns
daily_returns = data.pct_change()

# Calculate annual average returns and annual standard deviation (risk)
annual_returns = daily_returns.mean() * 252
annual_std = daily_returns.std() * np.sqrt(252)

# Convert to numpy arrays
assets_returns = annual_returns.values
assets_risk = annual_std.values

# Calculate the correlation matrix
correlation_matrix = daily_returns.corr().values

# Calculate the covariance matrix from annual standard deviation and correlation matrix
covariance_matrix = np.outer(assets_risk, assets_risk) * correlation_matrix

# Risk-free asset details
R_f = fetch_risk_free_rate()  # Risk-free rate

# Objective function to minimize (negative Sharpe Ratio)
def objective(weights):
    portfolio_return = np.dot(weights, assets_returns)
    portfolio_variance = np.dot(weights.T, np.dot(covariance_matrix, weights))
    portfolio_std = np.sqrt(portfolio_variance)
    sharpe_ratio = (portfolio_return - R_f) / portfolio_std
    return -sharpe_ratio  # Minimizing negative Sharpe Ratio is equivalent to maximizing it

# Constraints and bounds
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # The sum of weights is 1
bounds = tuple((0, 1) for _ in range(len(assets_returns)))  # Weights between 0 and 1

# Initial guess (equally weighted)
initial_guess = np.array([1. / len(assets_returns)] * len(assets_returns))

# Optimization
opt_result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

# Optimal weights for the risky assets
optimal_weights = opt_result.x

print("Optimal weights for the risky assets:", optimal_weights)
print("Expected return of the optimized risky portfolio:", np.dot(optimal_weights, assets_returns))

def optimize_portfolio_sharpe(stocks):
    # Download historical data
    data = yf.download(stocks, start='2023-01-01', end=datetime.today().strftime('%Y-%m-%d'))['Adj Close']
    
    # Calculate daily returns
    daily_returns = data.pct_change()
    
    # Calculate annual average returns and annual standard deviation (risk)
    annual_returns = daily_returns.mean() * 252
    annual_std = daily_returns.std() * np.sqrt(252)
    
    # Convert to numpy arrays
    assets_returns = annual_returns.values
    assets_risk = annual_std.values
    
    # Calculate the correlation matrix
    correlation_matrix = daily_returns.corr().values
    
    # Calculate the covariance matrix from annual standard deviation and correlation matrix
    covariance_matrix = np.outer(assets_risk, assets_risk) * correlation_matrix
    
    # Risk-free asset details
    R_f = fetch_risk_free_rate()  # Risk-free rate
    
    # Objective function to minimize (negative Sharpe Ratio)
    def objective(weights):
        portfolio_return = np.dot(weights, assets_returns)
        portfolio_variance = np.dot(weights.T, np.dot(covariance_matrix, weights))
        portfolio_std = np.sqrt(portfolio_variance)
        sharpe_ratio = (portfolio_return - R_f) / portfolio_std
        return -sharpe_ratio  # Minimizing negative Sharpe Ratio is equivalent to maximizing it
    
    # Constraints and bounds
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # The sum of weights is 1
    bounds = tuple((0, 1) for _ in range(len(assets_returns)))  # Weights between 0 and 1
    
    # Initial guess (equally weighted)
    initial_guess = np.array([1. / len(assets_returns)] * len(assets_returns))
    
    # Optimization
    opt_result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Optimal weights for the risky assets
    optimal_weights = opt_result.x
    
    # Expected return of the optimized portfolio
    expected_return = np.dot(optimal_weights, assets_returns)
    
    return {"optimal weights": optimal_weights, "expected return": expected_return}