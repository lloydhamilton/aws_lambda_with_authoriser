import requests
import json
from urllib.parse import urlparse
import datetime, hashlib, hmac
from src.logger import log_events

logger = log_events()

# Code adapted from https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html

# Key functions
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def sign_v4(method:str, endpoint:str, access_key:str, secret_key:str, data:dict, service:str, region:str):

    # ************* STEP 1: CREATE THE  CANONICAL HEADERS ***************
    # Create a date for headers and the credential string
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    parsed_url = urlparse(endpoint)

    # Canonical URI
    canonical_uri = parsed_url.path

    # Canonical query string
    canonical_querystring = parsed_url.query

    # Canonical headers
    host = parsed_url.netloc
    canonical_headers = (
        'host:' + host + '\n' +
        'x-amz-date:' + amz_date + '\n'
    )

    # Create the list of signed headers.
    signed_headers = 'host;x-amz-date'

    # Create payload hash
    payload_hash = hashlib.sha256(
        json
        .dumps(data)
        .encode('utf-8')
    ).hexdigest()

    # Combine elements
    canonical_request = (
        method + '\n' +
        canonical_uri + '\n' +
        canonical_querystring + '\n' +
        canonical_headers + '\n' +
        signed_headers + '\n' +
        payload_hash
    )

    # ************* TASK 2: CREATE THE STRING TO SIGN*************
    algorithm = 'AWS4-HMAC-SHA256'
    date_stamp = t.strftime('%Y%m%d')
    credential_scope = (
        date_stamp +
        '/' +
        region +
        '/' +
        service +
        '/' +
        'aws4_request'
    )
    string_to_sign = (
        algorithm + '\n' +
        amz_date + '\n' +
        credential_scope + '\n' +
        hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    )

    # ************* TASK 3: CALCULATE THE SIGNATURE *************
    # Create the signing key using the function defined above.
    signing_key = getSignatureKey(secret_key, date_stamp, region, service)

    # Sign the string_to_sign using the signing_key
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    #************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
    # Put the signature information in a header named Authorization.
    authorization_header = (
        algorithm + ' ' +
        'Credential=' + access_key + '/' + credential_scope + ', ' +
        'SignedHeaders=' + signed_headers + ', '
        + 'Signature=' + signature
    )

    headers = {
        'X-Amz-Date':amz_date,
        'Authorization':authorization_header
    }

    # ************* SEND THE REQUEST *************
    logger.info(f'\nBeginning {method} request to {endpoint}')
    r = requests.request(method=method, url=endpoint, json=data, headers=headers)
    logger.info('Response code: %d' % r.status_code)
    return r
