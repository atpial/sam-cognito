import os
import boto3
from dotenv import load_dotenv
load_dotenv()

region = os.getenv('COGNITO_REGION')
username = 'atahar.nur@shadhinlab.com'
password = 'gjNH46a2MEyjiTg'

client = boto3.client('cognito-idp', region)
response = client.initiate_auth(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    AuthFlow = 'USER_PASSWORD_AUTH',
    AuthParameters = {
        'USERNAME': username,
        'PASSWORD': password
    }
)
# print(response)

# print('AccessToken: ', response['AuthenticationResult']['AccessToken'])
# print('RefreshToken: ', response['AuthenticationResult']['RefreshToken'])

access_token = response['AuthenticationResult']['AccessToken']

valid_user = boto3.client('cognito-idp', region)
result = valid_user.get_user(
    AccessToken = access_token
)

# print(result)

user_name = None
email = None
for info in result['UserAttributes']:
    if info['Name'] == 'sub':
        user_name = info['Value']
        break
print(f"UserName:{user_name}")
for info in result['UserAttributes']:
    if info['Name'] == 'email':
        email = info['Value']
        break
print(f"Email:{email}")