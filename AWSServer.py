from server import app

PublicIP = '18.188.148.206'
AllIP = '0.0.0.0'
HTTPS = 443
HTTP = 80
context = ('www_ideoproject_net.crt', 'PRIVATEKEY.key')  # crt , key


if __name__ == '__main__':
    app.run(debug=False, host=PublicIP, port=HTTPS, ssl_context=context)