import boto3
import requests
import numpy as np
from aws_requests_auth.aws_auth import AWSRequestsAuth
import json
import sys, os, base64, datetime, hashlib, hmac

# AWS session keys
session = boto3.Session()
credentials = session.get_credentials()
access_key=credentials.access_key
secret_key=credentials.secret_key

# Key functions
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')

# ************* TASK 1: CREATE A CANONICAL REQUEST *************

# 1. Define verb
method = 'POST'

# 2. Create canonical URI--the part of the URI from domain to query.
canonical_uri = '/dev/predict'

# 3. Create the canonical query string.
canonical_querystring = ''

# 4. Create the canonical query string.
host = 'k1o73e73t4.execute-api.eu-west-2.amazonaws.com'
canonical_headers = (
    'host:' + host + '\n' +
    'x-amz-date:' + amz_date + '\n'
)

# 5. Create the list of signed headers.
signed_headers = 'host;x-amz-date'

# 6. Create payload hash
bucket_name = 'lh-lambda-buckets-202222'
key =  'validation/test_features.joblib'
data = {
    'bucket':bucket_name,
    'key':key,
}
payload_hash = hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()

# 7. Combine elements
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
service = 'execute-api'
region='eu-west-2'
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

# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
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

endpoint = 'https://k1o73e73t4.execute-api.eu-west-2.amazonaws.com/dev/predict'

# ************* SEND THE REQUEST *************
print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + endpoint)

data = {
    'bucket':bucket_name,
    'key':key,
}

r = requests.post(endpoint, json=data, headers=headers)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)
print(headers)

