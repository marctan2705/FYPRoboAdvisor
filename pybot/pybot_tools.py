from getpredictions import *
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from blacklitterman import *
from typing import List, Tuple, Dict, Union, Optional
from finance_api import * 
from collections import OrderedDict
from sharperatiooptimisation import *
class Company(BaseModel):
    company: str = Field(
        description="company user would like to find news about.")

class Portfolio_Stock(BaseModel):
    portfolio: List[str] = Field(
        description="list of stocks the user is interested in"
    )
class BLPort(BaseModel):
        portfolio_tickers: List[str] = Field(
        description="List of tickers of stocks the user is interested in"
    )
        portfolio_confidence: List[Tuple] = Field(
        description="Each tuple in the confidence list corresponds to the user's confidence in the view. The tuple consists of two floats: the lower bound (lb) and the upper bound (ub) of the expected return for that asset. These bounds represent the range within which the investor believes the actual return of the asset will fall, based on their view. you should always enter this as an upper and lower bound AROUND the view of the stock. For example, if a user thinks apple is gonna go 0.2, this should be to the effect of [x, y] where x < 0.2, y > 0.2"
    )
        portfolio_views: List[float] = Field(
        description="represents the views of the user. Each float corresponds to the user's view of the expected return from a stock. The position corresponds to that of portfolio_tickers "
    )
class searchModel(BaseModel):
     query: str = Field(
          description="This is the google search query"
     )
class stockModel(BaseModel):
        portfolio_tickers: List[str] = Field(
        description="List of tickers of stocks the user is interested in"
    )
        r_f: float = Field(
             description="risk free rate"
        )
class numberRoundModel(BaseModel):
    number: int = Field(
          description=" number that you want to round"
     )
class numberModel(BaseModel):
     a: int = Field(
          description="first number that you want to perform an operation on"
     )
     b: int = Field(
          description="second number that you want to perform an operation on"
     )
class Stocklist(BaseModel):
     stocklist: List[str] = Field(
          description="List of stocks that the user is interested in"
     )
@tool("analyse_stock", return_direct=False, args_schema=Company)
def sentiment_tool(company: str) -> str:
     """use this tool to analyse a stock's news"""
     tool = NewsSentimentTool()
     return tool.get_sentiment(company)

@tool("summarise_news", return_direct=False, args_schema=Company)
def retrive_news_tool(company: str) -> str:
    """Use this function to obtain news on companies the user is interested in"""
    newstool = NewsSummaryTool()
    res = newstool.get_summary(company)
    return res
@tool("ticker_finder", return_direct=False, args_schema=Portfolio_Stock)
def find_tickers_tool(portfolio: List[str]) -> str:
    """use this function to get the tickers of a portfolio of stocks the user is interested in"""
    res = []
    tickertool = TickerTool()
    for i in portfolio:
        res.append(tickertool.get_tickers(i)) 
    return res
@tool("portfolio_optimiser", return_direct=False, args_schema=BLPort)
def optimise_portfolio_tool(portfolio_tickers: List[str], portfolio_views: List[float], portfolio_confidence: List[Tuple]):
     """use this function to optimise a portfolio the user is interested in, after getting the stocks he is interested in, his views, and his confidence. you need to include all 3 parameters"""
    #  print("hi")  
     try:
        return getOptimal(portfolio_tickers, {portfolio_tickers[i]: portfolio_views[i] for i in range(len(portfolio_tickers))}, portfolio_confidence)
        #   return "hi"
     except:
          return "error, parameters check"
@tool("google_search", return_direct=False, args_schema=searchModel)
def search_tool(query: str) -> str:
     """use this tool to google information. This can be used to identify information."""
     google_tool  = GoogleSearchTool()
     return google_tool.search(query)

@tool("get_stock_data", return_direct=False, args_schema=stockModel)
def analysis__tool(r_f: float, portfolio_tickers: List[str]):
     "use this tool to get the price, beta and expected returns of a stock"
     tool = StockAnalysisTool(portfolio_tickers)
     return tool.analyse_stocks(r_f)

@tool("perform_addition", return_direct=False, args_schema=numberModel)
def addition_tool(a: float, b: float) -> float:
    "Use this tool to add two numbers"
    return a + b

@tool("perform_subtraction", return_direct=False, args_schema=numberModel)
def subtraction_tool(a: float, b: float) -> float:
    "Use this tool to subtract two numbers"
    return a - b

@tool("perform_multiplication", return_direct=False, args_schema=numberModel)
def multiplication_tool(a: float, b: float) -> float:
    "Use this tool to multiply two numbers"
    return a * b

@tool("perform_division", return_direct=False, args_schema=numberModel)
def division_tool(a: float, b: float) -> float:
    "Use this tool to divide two numbers"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@tool("perform_rounding", return_direct=False, args_schema=numberRoundModel)
def rounding_tool(a: float, digits: int) -> float:
    "Use this tool to round a number to a specified number of decimal places"
    return round(a, digits)

@tool("no_views_optimisation", return_direct=False, args_schema=Stocklist)
def rounding_tool(stocklist: List[str]):
    """use this function to optimise a portfolio if the user has no views nor confidence."""
    return optimize_portfolio_sharpe(stocklist)

tools = [sentiment_tool, retrive_news_tool, find_tickers_tool, optimise_portfolio_tool, search_tool, analysis__tool, addition_tool, multiplication_tool, subtraction_tool, division_tool, rounding_tool]

