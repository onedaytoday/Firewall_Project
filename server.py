from flask import Flask, request, json,render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route(rule='/')
def home_page():
    return render_template("hello.html")


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


#FLASK_APP=server.py flask run --cert=adhoc
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
if __name__ == "__main__":
    app.run()
    #app.run(ssl_context=('cert.pem', 'key.pem'))
    #app.run(ssl_context='adhoc')
