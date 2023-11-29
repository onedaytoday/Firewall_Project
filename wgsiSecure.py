import AWSServer
from server import app
if __name__ == '__main__':
    AWSServer.app.run(debug=False, host=AWSServer.PublicIP, port=AWSServer.HTTPS, ssl_context=AWSServer.context)
