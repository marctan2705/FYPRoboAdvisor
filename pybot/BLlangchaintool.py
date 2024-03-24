import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from pypfopt import risk_models, BlackLittermanModel, EfficientFrontier
from pypfopt import objective_functions, black_litterman
import json
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain.tools import BaseTool

from typing import List, Tuple, Dict, Union, Optional

class PortfolioOptimizerTool(BaseTool):
    name = "Portfolio Optimizer using Black-Litterman Model"
    description = "This tool optimizes a portfolio using the Black-Litterman model and Efficient Frontier optimization without needing initialization."

    def _run(self, portfolio: List[str], views: Dict[str, float], confidence: List[Tuple[float, float]], start_date: str = '2018-01-01'):
        """Main method to run the portfolio optimization process."""
        end_date = datetime.today().strftime('%Y-%m-%d')
        # Download data
        portfolio_prices = yf.download(portfolio, start=start_date, end=end_date)['Close']
        market_prices = yf.download('SPY', start=start_date, end=end_date)['Close']
        # Calculate market caps
        mcaps = {stock: yf.Ticker(stock).info["marketCap"] for stock in portfolio}
        # Calculate sigma (covariance matrix)
        sigma = risk_models.CovarianceShrinkage(portfolio_prices).ledoit_wolf()
        # Calculate delta (market-implied risk aversion)
        delta = black_litterman.market_implied_risk_aversion(market_prices)
        # Setup Black-Litterman model
        variances = [(ub - lb) / 2 for lb, ub in confidence]
        omega = np.diag([sigma_ind ** 2 for sigma_ind in variances])
        bl = BlackLittermanModel(sigma, pi="market", market_caps=mcaps, risk_aversion=delta, absolute_views=views, omega=omega)
        # Optimize portfolio
        ef = EfficientFrontier(bl.bl_returns(), bl.bl_cov())
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = ef.clean_weights()
        return weights
    def _arun(self, portfolio: List[str], views: Dict[str, float], confidence: List[Tuple[float, float]], start_date: str = '2018-01-01'):
        raise NotImplementedError("This tool does not support async")
    