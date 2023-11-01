import ipaddress
from flask import Flask, request, json, render_template, send_file
from flask_cors import CORS, cross_origin
import Errors
import auth
import Packet

keyVariableName = 'Api'
serialVariableName = 'Snum'
srcIPVariableName = 'srcIP'
destIPVariableName = 'destIP'
srcPortVariableName = 'srcPort'
destPortVariableName = 'destPort'
protocolVariableName = 'proto'

app = Flask(__name__)
cors = CORS(app)


@app.route(rule='/', methods=['GET'])
def home_page():
    print(request)
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
        MX = auth.MerakiDash(req.get(keyVariableName))
        MX.fetch_network(req.get(serialVariableName))
        MXFirewall = MX.get_firewall()
        MXFirewall.print()
        TestPacket = Packet.Packet(srcport=0,
                                   destport=0,
                                   source_ip=ipaddress.ip_address('172.16.1.4'),
                                   destination_ip=ipaddress.ip_address('172.16.2.1')
                                   )
        TestPacket.print()
        outcome = MXFirewall.filter(TestPacket)
        data = TestPacket.to_string() + " is " + outcome.get_value()
        response = Flask.response_class(
            response=data,
            status="202"
        )
        print(outcome)
    except Exception as e:
        response = Flask.response_class(
            error="Wrong APIKey",
            status="700"
        )
        return response
    return response


@app.route('/check', methods=['POST'])
def check_code_and_serial_and_firewall():
    req = request.get_json()
    print(request.get_json())
    try:
        MX = auth.MerakiDash(req.get(keyVariableName))
        MX.fetch_network(req.get(serialVariableName))
        MXFirewall = MX.get_firewall()
        #MXFirewall.print()
        TestPacket = Packet.Packet(srcport=req.get(srcPortVariableName),
                                   destport=req.get(destPortVariableName),
                                   source_ip=req.get(srcIPVariableName),
                                   destination_ip=req.get(destIPVariableName),
                                   protocol=req.get(protocolVariableName)
                                   )
        TestPacket.print()
        outcome, matched_rule = MXFirewall.find_matching_rule(TestPacket)
        print(outcome.get_value())
        output = json.dumps([outcome.get_value(), matched_rule.get_rule_json()])
        print(output)
        response = Flask.response_class(
            response = output,
            status="202"
        )
        print(outcome)
        return response
    except Exception as e:
        return respond_to_exception(e)


@app.route(rule='/check-key')
def check_key():
    try:
        req = request.get_json()
        auth.MerakiDash(req.get(serialVariableName))
        response = Flask.response_class(
            response=True,
            status="202"
        )
        return response
    except Exception as e:
        return respond_to_exception(e)


@app.route(rule='/check_key_and_serial')
def check_key_and_serial():
    try:
        req = request.get_json()
        dash = auth.MerakiDash(req.get(keyVariableName))
        dash.fetch_network(req.get(serialVariableName))
        response = Flask.response_class(
            response=True,
            status="202"
        )
        return response
    except Exception as e:
        respond_to_exception(e)


def respond_to_exception(e):
    Error = "Unknown Exception"
    Status = 700

    if isinstance(e, Errors.WrongDashKey):
        Error = "Wrong APIKey"
        Status = 701
    elif isinstance(e, Errors.WrongSerial):
        Error = "Wrong Serial"
        Status = 702
    elif isinstance(e, Errors.VLANProblems):
        Error = "Problem Getting VLANs"
        Status = 703
    elif isinstance(e, Errors.NoNetworkFound):
        Error = "Could not find Network"
        Status = 704
    elif isinstance(e, Errors.InvalidSourceIP):
        Error = "Invalid Source IP"
        Status = 705

    elif isinstance(e, Errors.InvalidDestinationIP):
        Error = "Invalid Destination IP"
        Status = 706
    elif isinstance(e, Errors.MissMatchedIPTypes):
        Error = "Mismatched IP types"
        Status = 707

    response = Flask.response_class(
        response=Error,
        status=str(Status)
    )
    return response


# FLASK_APP=server.py flask run --cert=adhoc
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
if __name__ == "__main__":
    # app.run()
    app.run(debug=False, host='0.0.0.0')
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    # app.run(ssl_context='adhoc')
