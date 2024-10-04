
from main import getData


def lambda_handler(event, context):
    # if 'RequestType' not in event or 'ResourceProperties' not in event:
    #     send_cfn_response(event, context, "FAILED", {}, "Cannot identify RequestType or ResourceProperties.")
    #     return


    return getData(event)

