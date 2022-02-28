import os
import boto3
import json

client = boto3.client('cognito-idp')

def forgot_pwd(username):
    response = client.forgot_password(
        ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
        Username=username,        
    )
    print('response: ',response)
    return response

def lambda_handler(event, context):
    # print(event)
    body = json.loads(event['body'])
    username = body["username"]
    try:
        result = forgot_pwd(username)
        return{
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
            'body': json.dumps({
            'error': False,
            'code': 'FORGOT_PASS_CODE_DELIVERED',
            'message': 'Forgot Password code deliver successful. To confirm please check email for confirmation code.',
            'value': result
            })
        }
    except client.exceptions.UserNotFoundException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'USER_NOT_FOUND',            
            'message': 'User could not be found with the provided email.'
            })
    }
    except client.exceptions.UserNotConfirmedException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'USER_NOT_CONFIRMED',
            'message': 'User not confirmed yet. Please check email for confirmation code'
            })
    }
    except client.exceptions.CodeDeliveryFailureException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code':'CODE_DELIVERY_FAILED',
            'message': 'failed to send confirmation code to the email.'
            })
        }
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'UNKNOWN_ERROR',
            'message': 'Some error occured. Please try again.'
            })
        }