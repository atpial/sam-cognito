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


















# import os
# import boto3
# from dotenv import load_dotenv
# load_dotenv()

# region = os.getenv('COGNITO_REGION')

# username = 'atp82232@gmail.com'
# password = '#Abcsas23234'

# client = boto3.client('cognito-idp', region)

# response = client.sign_up(
#     ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
#     Username = username,
#     Password = password,
#     UserAttributes=[{"Name": "email", "Value": username}]
# )

# print(response)

# # confirm_code = "841855"

# # result = client.confirm_sign_up(
# #     ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
# #     Username=username,
# #     ConfirmationCode=confirm_code,
# # )

# # print(result)