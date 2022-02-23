import os
import boto3
from dotenv import load_dotenv
load_dotenv()

region = os.getenv('COGNITO_REGION')

client = boto3.client('cognito-idp', region)

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2

def sign_up(username, password):
    try:
        response = client.sign_up(
            ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
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
    global client
    if client == None:
        client = boto3.client('cognito-idp', region)

    print(event)
    body = event
    username = body['username']
    password = body['password']
    signed_up = sign_up(username, password)
    if signed_up == ERROR:
        return {'status': 'fail', 'msg': 'failed to sign up'}
    if signed_up == SUCCESS:
        return {'status': 'success', 'msg': 'sign up successful'}

