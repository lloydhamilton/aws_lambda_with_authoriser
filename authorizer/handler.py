def authorize(event, context):
    import jwt
    import logging

    # Define logger class
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('Authorising...')

    key = "dancingPotatoes_!"
    auth = 'Deny'
    code = event['authorizationToken']

    # Decode JSON Web Token
    try:
        jwt.decode(code, key, algorithms="HS256")
        auth = 'Allow'
        logger.info('Valid key. Authorised User...')
    except:
        auth ='Deny'
        logger.info('Invalid key. Unauthorised User...')

    # Policy document to return if authentication passes or fails
    methodArn = event['methodArn']
    authResponse = {
        "principalId": "abc123",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Resource": methodArn,
                "Effect": auth
            }]
        }
    }

    return authResponse