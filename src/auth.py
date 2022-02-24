import os
import boto3
import json

client = boto3.client('cognito-idp')

ERROR = 0
SUCCESS = 1

def authenticate(username, password):
    try:
        response = client.initiate_auth(
            ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
            AuthFlow = 'USER_PASSWORD_AUTH',
            Username=username,
            Password=password)
        print(response)
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']
        print('AccessToken: ',access_token)
        print('RefreshToken: ',refresh_token)
        return access_token, refresh_token
    except client.exceptions.UserNotFoundException as e:
        return ERROR
    except client.exceptions.UserNotConfirmedException as e:
        return ERROR
    except Exception as e:
        print(e)
        return ERROR
    return SUCCESS
    
def lambda_handler(event, context):

    print(event)
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    authenticated = authenticate(username, password)
    if authenticated == ERROR:
        return {'status': 'fail', 'msg': 'failed to authenticate user'}
    if authenticated == SUCCESS:
        return {'status': 'success', 'msg': 'authentication successful'}
