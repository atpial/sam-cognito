import os
import json
import boto3

client = boto3.client('cognito-idp')

def authenticate(username, password):
    response = client.initiate_auth(
        ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
        AuthFlow = 'USER_PASSWORD_AUTH',
        AuthParameters={
        'Username': username,
        'Password': password
         }
    )
    print(response)
    return response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    username = body["username"]
    password = body["password"]
    try:
        authenticated = authenticate(username, password)
        token = {
            'access_token' : authenticated['AuthenticationResult']['AccessToken'],
            'refresh_token' : authenticated['AuthenticationResult']['RefreshToken'],
            'id_token': authenticated['AuthenticationResult']['IdToken']
        }
        return{
            'statusCode': 200,
            'message': 'log in successful.',
            'token': token
        }
    except client.exceptions.UserNotConfirmedException as e:
        return {
            'statusCode': 400,
            'message': 'User not confirmed yet. Please check email for confirmation code'
    }
    except client.exceptions.InvalidPasswordException as e:
        return {
            'statusCode': 400,
            'message': 'Password is invalid. Please check again.'
        }
    except Exception as e:
        print(e)
        return{
            'message': 'Unknown Error'
        }
