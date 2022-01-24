import boto3
from src.logger import log_events

logger = log_events()

class Cognito:
    """Functions to authenticate with Cognito User client

    Parameters:
    username: str, username string of login details 
    password: str, password string of login details
    """
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password

    def login(self, client_id:str):
        client = boto3.client('cognito-idp')
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=client_id,
            AuthParameters={
                "USERNAME": self.username,
                "PASSWORD": self.password
            }
        )
        logger.info('Log in Successful')
        return response

    def get_token(self, client_id:str,):
        """Get access and id tokens of current login session via AWS Cognito

        Args:
            client_id (str): User pool client id of authenticating client.

        Returns:
            response (dict) : Response object of API authenticating call.
            access_token (str) : Access token encoded as a JSON web token.
            id_token (str) : Id token encoded as a JSON web token. Use this token in Authorization header when making API calls.
        """
        response = self.login(client_id)
        access_token = response['AuthenticationResult']['AccessToken']
        id_token = response['AuthenticationResult']['IdToken']
        return response, access_token, id_token

    def auth_challenge(self, client_id:str, new_password:str):
        """Authenticating challenge to change temporary password to a new user defined password.

        Args:
            client_id (str): User pool client id of authenticating client.
            new_password (str): Alpha numeric password containing one upper and one lower case letter

        Returns:
            challenge_resp (dict): Response object of API authenticating challenge.
        """
        resp = self.login(client_id)
        client = boto3.client('cognito-idp')
        challenge_resp = client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={
                'NEW_PASSWORD' : new_password,
                'USERNAME':self.username,
            },
            Session=resp['Session']
        )
        logger.info('Password Changed')
        return challenge_resp