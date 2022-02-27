import os
import boto3
import json

client = boto3.client('cognito-idp')


def confirm_log_in(username, confirm_code):

    response = client.confirm_sign_up(
        ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
        Username=username,
        ConfirmationCode=confirm_code)
    print(response)

    return response

def lambda_handler(event, context):

    print(event)
    body = json.loads(event['body'])
    username = body['username']
    confirm_code = body['confirm_code']
    try:
        confirmed = confirm_log_in(username, confirm_code)
        return{
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
            'body': json.dumps({
            'error': False,
            'code':'SIGNUP_CONFIRMED',
            'message': 'Sign up is confirmed',
            'value': confirmed
            })
        }
    except client.exceptions.CodeMismatchException as e:
        print(e)
        return{
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code':'INCORRECT_CODE',
            'message': 'confirmation code did not match.',
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
    except client.exceptions.ExpiredCodeException as e:
        print(e)
        return{
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code':'CODE_EXPIRED',
            'message': 'confirmation code is expired.',
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

