#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
model_id = 'anthropic.claude-3-5-sonnet-20241022-v2:0'
user_message = "How far is the moon from the planet earth, on average?"

conversation = [
            {
                "role": "user",
                "content": [{"text": user_message}],
                }
        ]

try:
    # Sending message to model with basic configuration.
    response = bedrock_client.converse(
            modelId = model_id,
            messages = conversation,
            inferenceConfig = {"maxTokens": 1024, "temperature": 0.4, "topP": 0.9}
            )

    # Extract and print the response
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError,Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
