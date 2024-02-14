import openai
import os
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "f36a79dd44ae795deff01f9fec894bbb5c8cd071f1e1f06d012e922a7bda761f"
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key="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")
API_KEY = "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"



def get_bot_response(messages):
    # print(messages)
    messagesedited = []
    for i in messages:
        if i["role"] == "system":
            messagesedited += [SystemMessage(content=i["content"])]
        elif i["role"] == "user":
            messagesedited += [HumanMessage(content=i["content"])]
        else:
            messagesedited += [AIMessage(content=i["content"])]
    response = chat(messagesedited)
    return response.content
    # openai.api_key = API_KEY

    # response = openai.ChatCompletion.create(
    #     model = "gpt-3.5-turbo",
    #     messages = messages
    # )
    # return response['choices'][0]['message']['content']

def google_search(query):
    llm = OpenAI(temperature=0, tiktoken_model_name="gpt-3.5-turbo", openai_api_key=API_KEY)
    tool_names = ["serpapi", "llm-math"]
    tools = load_tools(tool_names, llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose = True)
    return agent.run(query)

def get_news_sentiment(chatlog, company):
    template_qn = f'Could you summarise recent news on {company}?'
    news = google_search(template_qn)
    messagesedited = []
    for i in chatlog:
        if i["role"] == "system":
            messagesedited += [SystemMessage(content=i["content"])]
        elif i["role"] == "user":
            messagesedited += [HumanMessage(content=i["content"])]
        else:
            messagesedited += [AIMessage(content=i["content"])]
    messagesedited += [SystemMessage(content = f'given this news: {news}, what are your predictions on the tesla stock? Do you think the implications are positive or negative? Explain your thinking step by step in 5 sentences.')]
    response = chat(messagesedited)
    return response.content
# print(SystemMessage("You are a financial advisor who gives advice on investments"))
# print(get_news_sentiment("Tesla"))
