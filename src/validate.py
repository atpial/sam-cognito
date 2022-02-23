import os
import boto3
from dotenv import load_dotenv
load_dotenv()

region = os.getenv('COGNITO_REGION')

client = boto3.client('cognito-idp', region)

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2

def confirm_log_in(username, confirm_code):
    try:
        response = client.confirm_sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=username,
        ConfirmationCode=confirm_code)
        print(response)
    except client.exceptions.CodeMismatchException as e:
        return ERROR
    except client.exceptions.ExpiredCodeException as e:
        return ERROR
    except Exception as e:
        print(e)
        return ERROR
    return SUCCESS

def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp', region)

    print(event)
    body = event
    username = body['username']
    confirm_code = body['confirm_code']
    confirmed = confirm_log_in(username, confirm_code)
    if confirmed == ERROR:
        return {'status': 'fail', 'msg': 'failed to confirm sign up'}
    if confirmed == SUCCESS:
        return {'status': 'success', 'msg': 'sign up confirmed'}









# def lambda_handler(event, context):
#     if event['callerContext']['clientId'] == "<user pool app client id to be blocked>":
#         raise Exception("Cannot authenticate users from this user pool app client")

#     # Return to Amazon Cognito
#     return event