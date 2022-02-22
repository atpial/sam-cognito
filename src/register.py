import os
import boto3
from dotenv import load_dotenv
load_dotenv()

region = os.getenv('COGNITO_REGION')

username = 'atp82232@gmail.com'
password = '#Abcsas23234'

client = boto3.client('cognito-idp', region)

response = client.sign_up(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = username,
    Password = password,
    UserAttributes=[{"Name": "email", "Value": username}]
)

print(response)

# confirm_code = "841855"

# result = client.confirm_sign_up(
#     ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
#     Username=username,
#     ConfirmationCode=confirm_code,
# )

# print(result)