#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError

model_id = 'anthropic.claude-3-5-sonnet-20241022-v2:0'

system_prompt = [
            {
                'text': 'You are a bot that only returns translations from one language to another.'
                }
        ]

bedrock_client = boto3.client(service_name='bedrock-runtime')

temperature = 0.5
top_k = 200

inference_config = {"temperature": temperature}
additional_model_fields = {"top_k": top_k}

messages = []

doYouWantToContinue = True

print('Type your message to the chatbot below.\n\n')

while doYouWantToContinue == True:
    query = input('Human : ')
    model_input = {
                "role": "user",
                "content": [{"text": query}]
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
    print("AI : ",output_msg['content'][0]['text'])
    doYouWantToContinue = input('Do you want to continue? (Y/y) ')
    if doYouWantToContinue[0] == 'Y' or doYouWantToContinue[0] == 'y':
        doYouWantToContinue = True
    else:
        doYouWantToContinue = False
