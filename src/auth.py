import os
import boto3
from dotenv import load_dotenv
load_dotenv()

region = os.getenv('COGNITO_REGION')

client = boto3.client('cognito-idp', region)

ERROR = 0
SUCCESS = 1

def authenticate(username, password):
    try:
        response = client.initiate_auth(
            ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
            AuthFlow = 'USER_PASSWORD_AUTH',
            Username=username,
            Password=password)
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']
        print('AccessToken: ',access_token)
        print('RefreshToken: ',refresh_token)
    except client.exceptions.UserNotFoundException as e:
        return ERROR
    except client.exceptions.UserNotConfirmedException as e:
        return ERROR
    except Exception as e:
        print(e)
        return ERROR
    return SUCCESS
    
def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')

    print(event)
    body = event
    username = body['username']
    password = body['password']
    authenticated = authenticate(username, password)
    access_token = authenticated['AuthenticationResult']['AccessToken']
    refresh_token = authenticated['AuthenticationResult']['RefreshToken']
    if authenticated == ERROR:
        return {'status': 'fail', 'msg': 'failed to authenticate user'}
    if authenticated == SUCCESS:
        return {'status': 'success', 'msg': 'authentication successful',
                'AccessToken': access_token, 'RefreshToken': refresh_token}
