from flask import Flask, request, jsonify
from finance_api import *
from get_bot_response import *
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import certifi
from dotenv import load_dotenv
import os
from BLlangchaintool import *
import os
from getpredictions import *
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from blacklitterman import *
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from pybot_tools import tools
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from Portfolios import *
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
MONGO_URI =os.getenv("MONGO_URI")
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app,tlsCAFile=certifi.where())
memory = ConversationBufferMemory(return_messages=True)
# print(portfolios)
# agent = initialize_agenprint(portfolios)t(
# agent=AgentType.OPENAI_FUNCTIONS,
# tools=tools,
# llm=chat,
# verbose=True,
# max_iterations=3,
# early_stopping_method='generate',
# memory=ConversationBufferMemory(memory_key="chat_history")
# )
chat = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))
prompt = hub.pull("hwchase17/openai-tools-agent")
ag= create_openai_tools_agent(chat, tools, prompt)
agent = AgentExecutor.from_agent_and_tools(
agent=ag,
tools=tools,
llm=chat,
verbose=True,
max_iterations=3,
memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)
# print(agent)

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm = chat,
    verbose=True,
    memory=memory
)


def check_user(email, username):
    email_match = False if mongo.db.users.find_one({"email": email}) else True
    username_match = False if mongo.db.users.find_one({"username": username}) else True
    if email_match and username_match:
        return "Successful"
    if not email_match:
        return "Email is already tagged to an account"
    if not username_match:
        return "Username is already taken"
    # mongo.db.users.find(user)
    # find the user to see if username is available
print(agent.invoke({"input": "hi"}))
# mongo.init_app(app)
# print(mongo.db)
@app.route("/")
def home():
    return "Home"

@app.route("/get_context", methods = ['POST', 'OPTIONS'])
@cross_origin()
def get_context():
    agent.invoke({"input": f'use this context for the rest of the conversation: {request.get_json()["chatters"]["content"]}. Do not use tools unless you know all the parameters required.'})
    return "ok", 200

@app.route("/get_response", methods = ['POST', 'OPTIONS'])
@cross_origin()
def get_response():
    messages =  request.get_json()["chatters"]
    response = jsonify({"reply": agent.invoke({"input": messages[-1]["content"]})["output"]}) 
    return response, 200

@app.route("/add_user", methods = ['POST'])
@cross_origin()
def read_database():
    user_data = request.get_json()["user_data"]
    res = check_user(
        user_data["email"], user_data["username"]
    )
    user_collection = mongo.db.users
    if res == "Successful":
        user_collection.insert_one(user_data)
    return res, 200

@app.route("/find_user", methods = ['POST', 'OPTIONS'])
@cross_origin()
def user_return():
    user_data = request.get_json()["user_data"]
    user = mongo.db.users.find_one({'username': user_data['username']})
    print("user is:", user)
    if user:
        res = {
            'password': user['password']
        }
    else:
        res = {'password': None}
    return jsonify(res), 200

# @app.route("/add_user_details", methods = ['POST'])
# @cross_origin()
# def add_data():
#     user_data = request.get_json()["user_data"]
#     data_collection = mongo.db.user_data
#     data_collection.insert_one(user_data)
#     return "User data successfully added", 200

@app.route("/add_questionnaire", methods = ['POST'])
@cross_origin()
def add_questionnaire():
    user_data = request.get_json()["user_data"]
    data_collection = mongo.db.questionnaire
    data_collection.insert_one(user_data)
    return "User data successfully added", 200

@app.route("/add_assessment", methods = ['POST'])
@cross_origin()
def add_assessment():
    user_data = request.get_json()["user_data"]
    data_collection = mongo.db.risk_assessment
    data_collection.insert_one(user_data)
    return "User data successfully added", 200

@app.route("/get_questionnaire", methods = ['POST'])
@cross_origin()
def get_questionnaire():
    user_data = request.get_json()["user_data"]
    username = user_data["username"]
    print(username)
    q_collection = mongo.db.questionnaire
    res = q_collection.find_one(
        {'username': username}
    )
    if res:
        print(res)
        res = {
            'username': res["username"],
            'answers': res["answers"]
        }
        return jsonify(res), 200
    else:
        return jsonify({'questionnaire': False})
@app.route("/get_portfolio", methods = ['POST'])
@cross_origin()
def get_portfolio():
    user_data = request.get_json()["user_data"]
    print(user_data)
    risk = user_data["answers"]["risk"]
    investment = user_data["answers"]["investment horizon"]
    experience = user_data["answers"]["experience"]
    print(portfolios)
    portfolio = conversation(
         f"this is a list of portfolios: {portfolios}. User's risk tolerance is {risk} out of a hundred. His investment horizon is {investment} years. he has a {experience} level of experience. Recommend a portfolio to him from the list. Only return the name of the portfolio, do not return anything else. don't return a sentence."
        )
    print(portfolios[portfolio["response"]])
    data_collection = mongo.db.portfolios
    data = {
        "username": user_data["username"],
        "portfolio": {
            "name": portfolio["response"],
            "details": portfolios[portfolio["response"]]
        }
    }
    data_collection.insert_one(data)
    return jsonify({'done': True}), 200
@app.route("/retrieve_portfolio", methods = ['POST'])
@cross_origin()
def retrieve_portfolio():
    user_data = request.get_json()["user_data"]
    username = user_data["username"]
    print(username)
    q_collection = mongo.db.portfolios
    res = q_collection.find_one(
        {'username': username}
    )
    if res:
        print(res)
        res = {
            'portfolio': res["portfolio"],
        }
        return jsonify(res), 200
    else:
        return jsonify({'questionnaire': False})
if __name__ == "__main__":
    app.run(debug=True)

#ASK THE USER FOR INFORMATION ON HIMSELF
#CAN GET ARTICLES FROM CHATGPT AS SIMULATION
#CAN USE QUATERLY REPORTS ETC
#WHO IS THE TARGET AUDIENCE
#NET WORTH OF THE TARGET AUDIENCE