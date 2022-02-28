import os
import boto3
import json

client = boto3.client('cognito-idp')


def resend_confirm_code(username):

    response = client.resend_confirmation_code(
        ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
        Username=username,)
    print(response)

    return response

def lambda_handler(event, context):

    print(event)
    body = json.loads(event['body'])
    username = body['username']
    try:
        confirmed = resend_confirm_code(username)
        return{
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
            'body': json.dumps({
            'error': False,
            'code':'RESENDT_CONFIRMATIONCODE',
            'message': 'Confirmation code resent successful.Please check email for the code.',
            'value': confirmed
            })
        }
    except client.exceptions.NotAuthorizedException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'USER_NOT_AUTHORIZED',
            'message': 'Username or password is incorrect.Please try again.'
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

