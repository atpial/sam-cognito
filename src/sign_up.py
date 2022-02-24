import os
import boto3
import json

client = boto3.client('cognito-idp')

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2

def sign_up(username, password):
    try:
        response = client.sign_up(
            ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
            Username=username,
            Password=password)
        print(response)
    except client.exceptions.UsernameExistsException as e:
        return USER_EXISTS
    except client.exceptions.InvalidPasswordException as e:
        return ERROR
    except Exception as e:
        print(e)
        return ERROR
    return SUCCESS

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    username = body["username"]
    password = body["password"]
    signed_up = sign_up(username, password)
    if signed_up == ERROR:
        return {'status': 'fail', 'msg': 'failed to sign up'}
    if signed_up == SUCCESS:
        return {'status': 'success', 'msg': 'sign up successful'}

