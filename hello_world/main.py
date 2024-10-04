import json

import requests

try:
    ip = requests.get("http://checkip.amazonaws.com/")
except requests.RequestException as e:
    # Send some context about this error to Lambda Logs
    print(e)

    raise e

data = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "location": ip.text.replace("\n", "")
        }),
    }

def getData(evn):
    print(evn)
    return data