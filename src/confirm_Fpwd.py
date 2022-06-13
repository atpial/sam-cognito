import os
import boto3
import json

client = boto3.client("cognito-idp")


def confirm_forgot_pwd(username, confirm_code, password):

    response = client.confirm_forgot_password(
        ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
        Username=username,
        ConfirmationCode=confirm_code,
        Password=password,
    )
    print(response)

    return response


def lambda_handler(event, context):

    print(event)
    body = json.loads(event["body"])
    username = body["username"]
    confirm_code = body["confirm_code"]
    password = body["password"]
    header = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Content-Type": "application/json",
    }
    try:
        confirmed = confirm_forgot_pwd(username, confirm_code, password)
        return {
            "statusCode": 200,
            "headers": header,
            "body": json.dumps(
                {
                    "error": False,
                    "code": "PASSWORD_CHANGED",
                    "message": "Password change successful",
                    "value": confirmed,
                }
            ),
        }
    except client.exceptions.CodeMismatchException as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "INCORRECT_CODE",
                    "message": "confirmation code did not match.",
                }
            ),
        }
    except client.exceptions.CodeDeliveryFailureException as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "CODE_DELIVERY_FAILED",
                    "message": "failed to send confirmation code to the email.",
                }
            ),
        }
    except client.exceptions.NotAuthorizedException as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "USER_NOT_AUTHORIZED",
                    "message": "Username or password is incorrect.Please try again.",
                }
            ),
        }
    except client.exceptions.ExpiredCodeException as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "CODE_EXPIRED",
                    "message": "confirmation code is expired.",
                }
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": header,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "UNKNOWN_ERROR",
                    "message": "Some error occured. Please try again.",
                }
            ),
        }
