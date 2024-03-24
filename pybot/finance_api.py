import yfinance as yf
import pandas as pd
import numpy as np
import datetime
def calculate_historical_market_return(index_ticker):
        """
        Calculate the historical average annual return of a market index.
        
        :param index_ticker: The ticker symbol for the market index (e.g., '^GSPC').
        :param start_date: Start date for historical data (e.g., '2010-01-01').
        :param end_date: End date for historical data (e.g., '2020-01-01').
        :return: Historical average annual return of the index.
        """
        end_date = datetime.date.today()
        start_date = end_date - pd.DateOffset(months=2)
        index_data = yf.download(index_ticker, start=start_date, end=end_date)['Adj Close']
        index_returns = index_data.pct_change().dropna()
        avg_daily_return = index_returns.mean()
        avg_annual_return = (1 + avg_daily_return) ** 252 - 1  # Assuming 252 trading days in a year
        return avg_annual_return
class StockAnalysisTool:
    def __init__(self, stock_list):
        self.stock_list = stock_list
        self.price_data = {}

    def fetch_stock_data(self, stock):
        prices = yf.download(stock, period="1y", interval="1d", auto_adjust=True, threads=True)
        current_price = prices['Close'].iloc[-1]
        return prices['Close'], current_price

    def get_covariance_matrix(self):
        df = pd.DataFrame()
        for stock in self.stock_list:
            prices, _ = self.fetch_stock_data(stock)
            if df.empty:
                df = prices.to_frame(name=stock)
            else:
                df = df.join(prices.to_frame(name=stock), how='inner')
        return df.cov()

    def analyse_stocks(self, risk_free_rate):
        prices = {}
        betas = {}
        expected_returns = {}
        
        # Fetch market data for beta calculation
        market_prices, _ = self.fetch_stock_data("SPY")

        for stock in self.stock_list:
            prices_over_year, current_price = self.fetch_stock_data(stock)
            prices[stock] = current_price
            betas[stock] = self.get_beta(prices_over_year, market_prices)
            expected_returns[stock] = self.calculate_expected_return(
                betas[stock], risk_free_rate, calculate_historical_market_return("SPY"))

        covariance_matrix = self.get_covariance_matrix()
        return {"prices": prices, "betas": betas, "expected_returns": expected_returns, "covariance_matrix": covariance_matrix}

    def get_beta(self, stock_prices, market_prices):
        covariance = np.cov(stock_prices, market_prices)[0][1]
        market_variance = market_prices.var()
        beta = covariance / market_variance
        return beta
    
    def calculate_expected_return(self, beta, risk_free_rate, expected_market_return):
        return risk_free_rate + beta * (expected_market_return - risk_free_rate)
