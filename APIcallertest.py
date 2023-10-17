# API caller test

import requests
import json


class API:  # API caller class
    def APIinput(self):  # Sends user GET request to the API server and returns status code
        APIcall = requests.get(input("Please enter an API url to send the GET request to: "))
        self.status = APIcall.status_code
        self.json = APIcall.json()
        print(APIcall.status_code)

    def jsonFormat(self):  # Dumps json to string, formats it, and prints it to terminal
        text = json.dumps(self.json, sort_keys=True, indent=4)
        print(text)


if __name__ == '__main__': # Calls object methods
    obj = API()
    obj.APIinput()
    obj.jsonFormat()
