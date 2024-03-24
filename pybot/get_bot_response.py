import openai
import os
from langchain.llms import OpenAI
from dotenv import load_dotenv
from BLlangchaintool import *
import os
from getpredictions import *

load_dotenv()

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")÷
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
print(os.getenv("OPENAI_API_KEY"))
# chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))
# tools = [create_tools_search()] + [createbltool(), makestocktool()]
# chat.bind(tools=tools)



def get_bot_response(chat, messages):
    # messagesedited = []
    # for i in messages:
    #     print(i)
    #     if i["role"] == "system":
    #         messagesedited += [SystemMessage(content=i["content"])]
    #     elif i["role"] == "user":
    #         messagesedited += [HumanMessage(content=i["content"])]
    #     else:
    #         messagesedited += [AIMessage(content=i["content"])]
    response = chat.run(input=messages[-1]["content"])
    return response
