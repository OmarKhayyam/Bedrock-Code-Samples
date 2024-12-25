#!/usr/bin/python3

# This is not just a chat with a knowledge base but also 
# maintains a memory of previous interactions (not earlier chat sessions)

import boto3
import json

# Use this command to find the modelArn:
# aws bedrock get-foundation-model --model-identifier anthropic.claude-3-5-sonnet-20241022-v2:0
model_arn = "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
knowledgebase_id = 'CDJTKBIXDP'
system_prompt = [
            {
                'text': 'You are an app that responds to queries relating only to Indian corporate law.'
                }
        ]

client = boto3.client('bedrock-agent-runtime')

#temperature = 0.7
#top_k = 200

#inference_config = {"temperature": temperature}
#additional_model_fields = {"top_k": top_k}

messages = system_prompt[0]['text']

doYouWantToContinue = True

print('Type your message to the chatbot below.\n\n')

while doYouWantToContinue == True:
    query = input('\nHuman : ')
    messages += messages + ' ' + query
    model_input = {
            "text": messages
            }
    RnGConfiguration = {
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': knowledgebase_id,
            'modelArn': model_arn
            }
            }

    response = client.retrieve_and_generate(
            input=model_input, # changed from messages, how do we keep track of what we said before?
            retrieveAndGenerateConfiguration = RnGConfiguration
            )
    output_msg = response['output']['text']
    messages += output_msg
    print("AI : ",output_msg)
    doYouWantToContinue = input('\nDo you want to continue? (Y/y) ')
    if doYouWantToContinue[0] == 'Y' or doYouWantToContinue[0] == 'y':
        doYouWantToContinue = True
    else:
        doYouWantToContinue = False
