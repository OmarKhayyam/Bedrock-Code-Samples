#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

chat = ChatBedrock(
    model_id = 'anthropic.claude-3-5-sonnet-20241022-v2:0',
    model_kwargs = {'temperature': 0.3}
        )

#messages = [
#    HumanMessage(
#        content="Translate this sentence from English to French. I love programming."
#    )
#]
#response = chat.invoke(messages)

#print("AI : ",response.content)

doYouWantToContinue = True

print('Type your message to the chatbot below.\n\n')

##while doYouWantToContinue == True:
##    humanmsg = input('Human : ')
##    message = [
##    HumanMessage(
##        content=humanmsg
##    )
##    ]
##    response = chat.invoke(message)
##    print('AI : ',response.content,'\n')
##    doYouWantToContinue = input('Do you want to continue? (Y/y) ')
##    if doYouWantToContinue[0] == 'Y' or doYouWantToContinue[0] == 'y':
##        doYouWantToContinue = True
##    else:
##        doYouWantToContinue = False


prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions to the best of your ability."
                    ),
                MessagesPlaceholder(variable_name='chat_history'),
                ("human","{input}")
                ]
        )

chain = prompt | chat

ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: ephemeral_chat_history_for_chain,
        input_messages_key = "input",
        history_messages_key = "chat_history"
        )

while doYouWantToContinue == True:
    humanmsg = input('Human : ')
    message = [
    HumanMessage(
        content=humanmsg
    )
    ]
    response = chain_with_message_history.invoke(
            {"input": message},
            {"configurable": {"session_id": "unused"}}
            )
    print('AI : ',response.content,'\n')
    doYouWantToContinue = input('Do you want to continue? (Y/y) ')
    if doYouWantToContinue[0] == 'Y' or doYouWantToContinue[0] == 'y':
        doYouWantToContinue = True
    else:
        doYouWantToContinue = False

print('Thank you for the chat, I had a good time! Bye.')
