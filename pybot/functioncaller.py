import json

from langchain_core.utils.function_calling import convert_to_openai_tool

from typing import Any, Type

from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field


import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from pypfopt import risk_models, BlackLittermanModel, EfficientFrontier
from pypfopt import objective_functions, black_litterman

class PortfolioOptimizerBL:
    """
    This class provides functionality to optimize a portfolio using the Black-Litterman model
    and Efficient Frontier optimization.
    """
    def __init__(self, portfolio, views, confidence, start_date='2018-01-01'):
        self.portfolio = portfolio
        self.views = views
        self.confidence = confidence
        self.start_date = start_date
        self.end_date = datetime.today().strftime('%Y-%m-%d')
        self.market_prices = None
        self.portfolio_prices = None
        self.mcaps = {}
        self.sigma = None
        self.delta = None
        self.bl = None

    def download_data(self):
        """Download historical data for the portfolio and market index (SPY)."""
        self.portfolio_prices = yf.download(self.portfolio, start=self.start_date, end=self.end_date)['Close']
        self.market_prices = yf.download('SPY', start=self.start_date, end=self.end_date)['Close']

    def calculate_market_caps(self):
        """Calculate market capitalizations for the portfolio stocks."""
        for stock in self.portfolio:
            ticker = yf.Ticker(stock)
            self.mcaps[stock] = ticker.info["marketCap"]

    def calculate_sigma(self):
        """Calculate the covariance matrix for the portfolio."""
        self.sigma = risk_models.CovarianceShrinkage(self.portfolio_prices).ledoit_wolf()

    def calculate_delta(self):
        """Calculate the market-implied risk aversion."""
        self.delta = black_litterman.market_implied_risk_aversion(self.market_prices)

    def setup_black_litterman_model(self):
        """Setup the Black-Litterman model with the given views and confidences."""
        variances = [(ub - lb) / 2 for lb, ub in self.confidence]
        omega = np.diag([sigma_ind ** 2 for sigma_ind in variances])
        self.bl = BlackLittermanModel(self.sigma, pi="market", market_caps=self.mcaps,
                                      risk_aversion=self.delta, absolute_views=self.views, omega=omega)

    def optimize_portfolio(self):
        """Optimize the portfolio using the Efficient Frontier method."""
        ef = EfficientFrontier(self.bl.bl_returns(), self.bl.bl_cov())
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = ef.clean_weights()
        return weights

    def run_optimization(self):
        """Main method to run the optimization process."""
        self.download_data()
        self.calculate_market_caps()
        self.calculate_sigma()
        self.calculate_delta()
        self.setup_black_litterman_model()
        return self.optimize_portfolio()

print(json.dumps(convert_to_openai_tool(PortfolioOptimizerBL), indent=2))
optimizer = PortfolioOptimizerBL(portfolio=["AAPL", "TSLA"], views={"AAPL": 1.0, "TSLA": 2.0}, confidence=[(0, 2), (1, 2)])
optimized_weights = optimizer.run_optimization()
print(optimized_weights)