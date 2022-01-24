import boto3
# Def logging class
from src.logger import log_events

logger = log_events()

def cognito_login(client_id:str, username:str, password:str):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        ClientId=client_id,
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )
    logger.info('Log in Successful')
    return response

def cognito_get_token(client_id:str, username:str, password:str):
    response = cognito_login(client_id, username, password)
    access_token = response['AuthenticationResult']['AccessToken']
    id_token = response['AuthenticationResult']['IdToken']
    return response, access_token, id_token

def auth_challenge(client_id:str, username:str, current_pw:str, new_password:str):
    resp = cognito_login(client_id, username, current_pw)
    client = boto3.client('cognito-idp')
    challenge_resp = client.respond_to_auth_challenge(
        ClientId=client_id,
        ChallengeName='NEW_PASSWORD_REQUIRED',
        ChallengeResponses={
            'NEW_PASSWORD' : new_password,
            'USERNAME':username,
        },
        Session=resp['Session']
    )
    logger.info('Password Changed')
    return challenge_resp