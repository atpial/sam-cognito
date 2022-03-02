import os
import boto3
import json

client = boto3.client('cognito-idp')

def sign_up(username, password):
    response = client.sign_up(
        ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
        Username=username,
        Password=password,
        UserAttributes=[
        {
            'Name': 'email',
            'Value': username
        },
    ],        
    )
    print('response: ',response)
    return response

def lambda_handler(event, context):
    # print(event)
    body = json.loads(event['body'])
    username = body["username"]
    password = body["password"]
    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json',        
    }
    try:
        signed_up = sign_up(username, password)
        return{
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
            'error': False,
            'code':'SIGN_UP_SUCCESSFUL',
            'message': 'Sign up is successful. To confirm please check email for confirmation code.',
            'value': signed_up
            })
        }
    except client.exceptions.UsernameExistsException as e:
        print(e)
        return {
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
            'error': True,
            'code': 'USERNAME_EXISTS',
            'message': 'Username already exists'
            })
    }
    except client.exceptions.InvalidPasswordException as e:
        print(e)
        return {
            'statusCode': 400,
            'headers': header,
            'error': True,
            'code': 'INVALID_PASSWORD',
            'body': json.dumps({
            'message': 'Password is invalid. Please check again.'
            })
        }
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({
            'error': True,
            'code': 'UNKNOWN_ERROR',
            'message': 'Some error occured. Please try again.'
            })
        }