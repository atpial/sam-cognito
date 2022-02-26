import os
import json
import boto3

client = boto3.client('cognito-idp')

def authenticate(username, password):
    response = client.initiate_auth(
        ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
        AuthFlow = 'USER_PASSWORD_AUTH',
        AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
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
            'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://www.example.com',
            'Access-Control-Allow-Methods': 'PUT,POST,GET'
        },
            'body': json.dumps({
            'message': 'log in successful.',
            'token': token
            })
        }
    except client.exceptions.UserNotConfirmedException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
            'message': 'User not confirmed yet. Please check email for confirmation code'
            })
    }
    except client.exceptions.UserNotFoundException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
            'message': 'User could not be found.Please check username/password.'
            })
        }
    except client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
            'message': 'Username or password is incorrect.Please try again.'
            })
        }
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'body': json.dumps({
            'message': 'Some error occured. Please try again.'
            })
        }
