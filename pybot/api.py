from flask import Flask, request, jsonify
from finance_api import *
from get_bot_response import *
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import certifi

messages = [
                {"role":"system", "content":"You are a financial assistant specialised in giving advice on how to allocate a portfolio with minimum risk and providing information about various stocks."}
]
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
MONGO_URI ='mongodb+srv://secretshop:QIjkwdCzTLCHprX7@cluster0.ypxj3dl.mongodb.net/FYP?retryWrites=true&w=majority&tls=true'
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app,tlsCAFile=certifi.where())

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

# mongo.init_app(app)
# print(mongo.db)
@app.route("/")
def home():
    return "Home"

@app.route("/get_ticker/<stock>")
def get_ticker(stock):
    ticker = getTicker(stock)
    res = {
        "ticker": ticker
    }
    return jsonify(res), 200

@app.route("/get_response", methods = ['POST', 'OPTIONS'])
@cross_origin()
def get_response():
    messages.append({"role": "user", "content": request.get_json()["chatters"]})
    botResponse = get_bot_response(messages)
    response = jsonify({"reply": botResponse}) 
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

@app.route("/add_user_details", methods = ['POST'])
@cross_origin()
def add_data():
    user_data = request.get_json()["user_data"]
    data_collection = mongo.db.user_data
    data_collection.insert_one(user_data)
    return "User data successfully added", 200

@app.route("/add_questionnaire", methods = ['POST'])
@cross_origin()
def add_questionnaire():
    user_data = request.get_json()["user_data"]
    data_collection = mongo.db.questionnaire
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
if __name__ == "__main__":
    app.run(debug=True)

#ASK THE USER FOR INFORMATION ON HIMSELF
#CAN GET ARTICLES FROM CHATGPT AS SIMULATION
#CAN USE QUATERLY REPORTS ETC
#WHO IS THE TARGET AUDIENCE
#NET WORTH OF THE TARGET AUDIENCE