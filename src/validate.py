import os
import boto3
import json

client = boto3.client('cognito-idp')

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2

def confirm_log_in(username, confirm_code):
    try:
        response = client.confirm_sign_up(
        ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
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
    return response

def lambda_handler(event, context):

    print(event)
    body = json.loads(event['body'])
    username = body['username']
    confirm_code = body['confirm_code']
    confirmed = confirm_log_in(username, confirm_code)
    if confirmed == ERROR:
        return {'status': 'fail', 'msg': 'failed to confirm sign up'}
    if confirmed == SUCCESS:
        return {'status': 'success', 'msg': 'sign up confirmed'}

