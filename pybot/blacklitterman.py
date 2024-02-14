import numpy as np
# from scipy.optimize import minimize
import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# import seaborn as sb
from pypfopt import *
from finance_api import *
import yfinance as yf
from datetime import date
from pypfopt import risk_models, BlackLittermanModel, DiscreteAllocation
from pypfopt import EfficientFrontier, objective_functions, black_litterman
# print("hi")

def getBL(portfolio, views, confidence):
    # plt.style.available
    portfolio_prices = yf.download(portfolio, start='2018-01-01', end = date.today())['Close']
    market_prices = yf.download('SPY', start='2018-01-01', end = date.today())['Close']
    mcaps = {}
    for stock in portfolio:
        ticker = yf.Ticker(stock)
        mcaps[stock] = ticker.info["marketCap"]
    sigma = getSigma(portfolio_prices)
    delta = getDelta(market_prices)
    variances = []
    for lb, ub in confidence:
        sigma_ind = (ub - lb)/2
        variances += [sigma_ind ** 2]
    omega = np.diag(variances)
    bl = BlackLittermanModel(sigma, pi="market", market_caps = mcaps, risk_aversion=delta, absolute_views=views, omega=omega)
    return bl

def getBLReturns(bl):
    return bl.bl_returns()

def getBLCov(bl):
    return bl.bl_cov()

def effFrontier(bl):
    ef = EfficientFrontier(getBLReturns(bl), getBLCov(bl))
    ef.add_objective(objective_functions.L2_reg)
    ef.max_sharpe()
    weights = ef.clean_weights()
    return weights

        
def getSigma(portfolio_prices):
    sigma = risk_models.CovarianceShrinkage(portfolio_prices).ledoit_wolf()
    return sigma

def getDelta(market_prices):
    delta = black_litterman.market_implied_risk_aversion(market_prices)
    return delta

eff = effFrontier(getBL(["AAPL", "TSLA"], {"AAPL": 1.0, "TSLA": 2.0}, [(0,2), (1,2)]))
print(eff)