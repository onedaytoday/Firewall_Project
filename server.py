from flask import Flask, request, json,render_template
from flask_cors import CORS, cross_origin

import IPaddress
import auth
import Packet

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
    print(request.get_json().get('code'))

    data = "SecretCode"
    response = Flask.response_class(
        response=data,
        status="202"
    )
    return response


@app.route('/test', methods=['POST'])
def test_code_and_serial():
    req = request.get_json()
    print(request.get_json())
    try:
        MX = auth.MerakiDash(req.get('code'), req.get('serial'))
        MXFirewall = MX.get_firewall()
        MXFirewall.print()
        TestPacket = Packet.Packet(srcport=0,
                                   destport=0,
                                   source_ip=IPaddress.IPAddress.make_ip_from_dot_notation_ip_string('172.16.1.4'),
                                   destination_ip=IPaddress.IPAddress.make_ip_from_dot_notation_ip_string('172.16.2.1')
                                   )
        TestPacket.print()
        outcome = MXFirewall.filter(TestPacket)
        data = outcome.get_value()
        response = Flask.response_class(
            response=data,
            status="202"
        )
        print(outcome)
    except:
        data = "Failed"
        response = Flask.response_class(
        response=data,
        status="700"
        )
        return response
    return response


#FLASK_APP=server.py flask run --cert=adhoc
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
if __name__ == "__main__":
    app.run()
    #app.run(ssl_context=('cert.pem', 'key.pem'))
    #app.run(ssl_context='adhoc')
