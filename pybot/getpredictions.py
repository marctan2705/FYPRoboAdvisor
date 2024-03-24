import openai
import os
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from dotenv import load_dotenv
from langchain_core.utils.function_calling import convert_to_openai_tool
load_dotenv()
chat = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

class GoogleSearchTool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = None
        self.agent = None

    def setup(self):
        self.llm = OpenAI(temperature=0, tiktoken_model_name="gpt-4-0125-preview", openai_api_key=self.api_key)
        tool_names = ["serpapi", "llm-math"]
        tools = load_tools(tool_names, self.llm)
        self.agent = initialize_agent(tools, self.llm, agent="zero-shot-react-description", verbose=True)

    def search(self, query):
        if not self.agent:
            self.setup()
        return self.agent.run(query)

class NewsSummaryTool:
    def __init__(self):
        self.search_tool = GoogleSearchTool(api_key=os.getenv("OPENAI_API_KEY"))

    def get_summary(self, company):
        template_qn = f'What is the news on {company}?'
        news = self.search_tool.search(template_qn)
        return news

class TickerTool:
    def __init__(self):
        self.search_tool = GoogleSearchTool(api_key=os.getenv("OPENAI_API_KEY"))

    def get_tickers(self, companies):
        template_qn = f'Could you find the tickers of {companies}?'
        tickers = self.search_tool.search(template_qn)
        return tickers
    
class NewsSentimentTool:
    def __init__(self):
        self.summary_tool = NewsSummaryTool()

    def get_sentiment(self, company):
        news = self.summary_tool.get_summary(company)
        messages = [SystemMessage(content='you are a highly knowledgeable financial advisor who specialises in financial analyses and risk management'),
                    HumanMessage(content=f'Given this news: {news}, can you analyse whether this is positive or negative sentiments? do you think this is good or bad for apple.')]
        response = chat(messages)
        return response.content

# def create_tools_search():
#     return [convert_to_openai_tool(GoogleSearchTool), convert_to_openai_tool(NewsSummaryTool), convert_to_openai_tool(NewsSummaryTool)]