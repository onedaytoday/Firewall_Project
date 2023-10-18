from flask import Flask, request, json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)




@app.route('/', methods=['POST'])
def default_handler():
    print("Default")
    response = Flask.response_class(
        response="Y",
        status="201"
    )
    return response


@app.route('/server', methods=['POST'])
def server_request_handler():
    print(request.get_data().decode())
    print(request.get_json())

    data = "SecretCode"
    response = Flask.response_class(
        response=data,
        status="202"
    )
    return response
