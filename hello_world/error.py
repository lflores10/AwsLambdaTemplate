import json
import requests


def send_cfn_response(event, context, response_status, response_data, reason):
    response_body = {'Status': response_status,
                    'Reason': 'Log stream name: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': response_data}
    print("Log Reason: " + reason)
    try:
        requests.put(event['ResponseURL'], data=json.dumps(response_body))
    except Exception as e:
        print(e)
        raise