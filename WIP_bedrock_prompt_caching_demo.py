#!/usr/bin/python3

## This demonstrates the use of prompt caching in Anthropic Sonnet V2 model.
## This example is for message prompts.

###############
###***WIP***###
###############

import os
import base64
import boto3
from botocore.exceptions import ClientError

def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

model_id = 'anthropic.claude-3-5-sonnet-20241022-v2:0'

system_prompt = [
            {
                'text': 'You are a bot that describes images. Avoid profanity and any kind of prejudice regarding the subjects color, race or religion. You should also avoid being overly creative in your description, stick to simple english. You can ocacssionally use french or latin for impact. From the image provided, provide a detailed description of the image.'
                },
            {
                'cachePoint': {
                    "type": "default"
                    }
                }
        ]

bedrock_client = boto3.client(service_name='bedrock-runtime')

temperature = 0.5
top_k = 200

inference_config = {"temperature": temperature}
additional_model_fields = {"top_k": top_k}

messages = []

print('*******************************************\n')
print('****Type your message to the bot below.****\n')
print('*******************************************\n\n')

for fl in iterate_files(os.path.join(os.getcwd(), 'images')):
    print("Looking at this image: ",fl)
    f = open(fl,'rb')
    query = input('Human : ')
    ## be specific what type of cachePoint this is.
    model_input = {
            "role": "user",
            "content": [
                    {
                        "text": query
                        }
                ]
            }
    messages.append(model_input)
    response = bedrock_client.converse(
                modelId = model_id,
                messages = messages,
                system = system_prompt,
                inferenceConfig = inference_config,
                additionalModelRequestFields = additional_model_fields
            )
    output_msg = response['output']['message']
    messages.append(output_msg)

