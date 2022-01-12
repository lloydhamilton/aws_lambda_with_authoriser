import boto3
import requests
import numpy as np
from aws_requests_auth.aws_auth import AWSRequestsAuth

import sys, os, base64, datetime, hashlib, hmac
import requests

# Values
method = 'POST'
service = 'execute-api'
host='k1o73e73t4.execute-api.eu-west-2.amazonaws.com'
region='eu-west-2'

# Aws session keys
session = boto3.Session()
credentials = session.get_credentials()
access_key=credentials.access_key
secret_access_key=credentials.secret_key

# Key functions 
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning








bucket_name = 'lh-lambda-buckets-202222'
key =  'validation/test_features.joblib'

data = {
    'bucket':bucket_name,
    'key':key,
}

session = boto3.Session()
credentials = session.get_credentials()

auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                       aws_secret_access_key=credentials.secret_key,
                       aws_token=credentials.token,
                       aws_host='k1o73e73t4.execute-api.eu-west-2.amazonaws.com',
                       aws_region='eu-west-2',
                       aws_service='execute-api')

# canonical_uri = '/dev/predict'
response = requests.post('https://k1o73e73t4.execute-api.eu-west-2.amazonaws.com/dev/predict',json=data, auth=auth)

print(np.array(response.json()))

