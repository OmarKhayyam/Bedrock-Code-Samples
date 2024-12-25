#!/usr/bin/python3

import json
import boto3

def list_foundation_models():
    bedrock = boto3.client(service_name='bedrock', region_name='us-west-2')
    response = bedrock.list_foundation_models()
    return response

print(json.dumps(list_foundation_models(), indent = 1))
