import yfinance as yf
import pandas as pd
import numpy as np
from get_bot_response import *

###### i need current price, expected returns, variance, covariance #####

def analyseStocks(stockList):
    prices = {}
    dfExist = False
    betas = {

    }
    for stock in stockList:
        stockdata = fetchStockData(stock)
        prices[stock] += stockdata["price"]
        if not dfExist:
            priceData = stockdata["pricesoveryear"]
        else:
            pd.merge(priceData, stockdata["prices"])
        betas[stock] = getBeta(stockdata["pricesoveryear"].tolist())
    covarianceMatrix = getCovarianceMatrix(priceData)
    return {
        "prices": prices,
        "betas": betas,
        "covmatrix": covarianceMatrix
    }
        

def getTicker(stock):
    prompt = f'What is the stock symbol for {stock}'
    return google_search(prompt)

def getTickerInfo(stock):
    ticker = yf.Ticker(getTicker(stock))


def getStockNews(ticker):
    news = ticker.news
    return news

def fetchStockData(stock):
    prices = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = stock,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "1y",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )
    mrp = prices.loc[prices.index == prices.index.max().strftime('%Y-%m-%d')].Close
    return {"price": mrp, "pricesoveryear": prices["Close"]}


def getCovarianceMatrix(df):
    return df.cov()

def getBeta(pricesoveryear):
    indexData = fetchStockData("SPY")
    covariance = np.cov(pricesoveryear, indexData["Close"].tolist())
    idxStkCov = covariance[0][1]
    idxVariance = covariance[1][1]
    beta = idxStkCov/idxVariance
    return beta
    