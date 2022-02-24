import os
import json
import boto3

client = boto3.client('cognito-idp')

ERROR = 0
SUCCESS = 1

def log_in(username, password):
    try:
        response = client.sign_up(
            ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
            Username=username,
            Password=password)
        print(response)
    except client.exceptions.InvalidPasswordException as e:
        return ERROR
    except client.exceptions.NotAuthorizedException as e:
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
    logged_in = log_in(username, password)
    if logged_in == ERROR:
        return {'status': 'fail', 'msg': 'failed to log in'}
    if logged_in == SUCCESS:
        return {'status': 'success', 'msg': 'log in successful'}
