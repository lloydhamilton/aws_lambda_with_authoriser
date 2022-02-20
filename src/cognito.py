import boto3
from src.logger import log_events

class Cognito:
    """Functions to manage Cognito user pool

    Args:
        username (str): username string of login detail or intended login detail

    """
    def __init__(self, username:str):
        if not isinstance(username, str):
            raise ValueError(f'Username must be of type str, got:{type(username)}')
        self.username = username
        self.client = boto3.client('cognito-idp')
        self.logger = log_events()

    def create_user(self, userpoolid:str) -> dict:
        """Create user using an email as username. create_user will require admin permissions.

        Args:
            userpoolid (str): User pool ID for user creation.

        Returns:
            dict: Response object of API.
        """
        resp = self.client.admin_create_user(
            UserPoolId = userpoolid,
            Username = self.username,
            DesiredDeliveryMediums=['EMAIL']
        )
        return resp

    def login(self, client_id:str, password:str):
        response = self.client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=client_id,
            AuthParameters={
                "USERNAME": self.username,
                "PASSWORD": password
            }
        )
        self.logger.info('Log in Successful')
        return response

    def get_token(self, client_id:str, password:str):
        """Get access and id tokens of current login session via AWS Cognito

        Args:
            client_id (str): User pool client id of authenticating client.
            password (str): Password string for login.

        Returns:
            response (dict) : Response object of API authenticating call.
            access_token (str) : Access token encoded as a JSON web token.
            id_token (str) : Id token encoded as a JSON web token. Use this token in Authorization header when making API calls.
        """
        response = self.login(client_id, password)
        access_token = response['AuthenticationResult']['AccessToken']
        id_token = response['AuthenticationResult']['IdToken']
        return response, access_token, id_token

    def auth_challenge(self, client_id:str, password:str, new_password:str) -> dict:
        """Authenticating challenge to change temporary password to a new user defined password.

        Args:
            client_id (str): User pool client id of authenticating client.
            password (str): Current password string for login.
            new_password (str): Password must contain at least:
                                6 characters
                                One upper case letter
                                One lower case letter
                                One symbol
                                One number

        Returns:
            challenge_resp (dict): Response object of API authenticating challenge.
        """
        resp = self.login(client_id, password)
        challenge_resp = self.client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={
                'NEW_PASSWORD' : new_password,
                'USERNAME':self.username,
            },
            Session=resp['Session']
        )
        self.logger.info('Password Changed')
        return challenge_resp

# test for exceptions
