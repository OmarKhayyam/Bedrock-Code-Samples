#!/usr/bin/python3

import time
import boto3
from botocore.exceptions import ClientError

# We will be using the following Kaggle dataset:
# https://www.kaggle.com/datasets/thejas2002/prompt
# aka AutoAIQnA: QNA for Automobile Specs
# Source: kaggle.com


###$$%%*********%%$$###
###$$%%** WIP **%%$$###
###$$%%*********%%$$###

# Steps:
# Find a Foundation model we can fine-tune.
# Make sure the dataset is set up correctly so as to enable us to fine-tune said model.
# Run a fine-tuning job. Check result.
# Deploy the model, if we can, and try how it performs compared to the non-fine-tuned model.

region = "us-west-2"
br_cl = boto3.client(service_name="bedrock", region_name = region)

def get_fine_tunables():
    for model in br_cl.list_foundation_models(byCustomizationType = "FINE_TUNING")["modelSummaries"]:
        for key, value in model.items():
            print(key,": ",value)
        print("-----\n")

#get_fine_tunables()

role_name = "RNS-Bedrock-Fine-Tuning-Role"

iam = boto3.client('iam', region_name=region)

def check_role(role_name):
    try:
        response = iam.get_role(RoleName=role_name)
        return True
    except:
        return False

## Setting up IAM policy for Bedrock based finetuning

sts_client = boto3.client('sts')
account_id = sts_client.get_caller_identity()["Account"]
bucket_name = "rns-bedrock-documents"

ROLE_DOC = f"""{{
    "Version": "2012-10-17",
    "Statement": [
        {{
            "Effect": "Allow",
            "Principal": {{
                "Service": "bedrock.amazonaws.com"
            }},
            "Action": "sts:AssumeRole",
            "Condition": {{
                "StringEquals": {{
                    "aws:SourceAccount": "{account_id}"
                }},
                "ArnEquals": {{
                    "aws:SourceArn": "arn:aws:bedrock:{region}:{account_id}:model-customization-job/*"
                }}
            }}
        }}
    ]
}}
"""

ACCESS_POLICY_DOC = f"""{{
    "Version": "2012-10-17",
    "Statement": [
        {{
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetBucketAcl",
                "s3:GetBucketNotification",
                "s3:ListBucket",
                "s3:PutBucketNotification"
            ],
            "Resource": [
                "arn:aws:s3:::{bucket_name}",
                "arn:aws:s3:::{bucket_name}/*"
                "arn:aws:s3:::{bucket_name}/*/*"
            ]
        }}
    ]
}}"""

s3_bedrock_finetuning_access_policy = "RNS-Bedrock-Finetuning-Policy"
role_arn = ""

if not check_role(role_name):
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=ROLE_DOC,
        Description="Role for Bedrock to access S3 for haiku finetuning",
    )

    rolearn = response["Role"]["Arn"]
    print("RoleArn: ",rolearn)
    role_arn = rolearn
    # This does not seem to be working. It is required.
    response = iam.create_policy(
        PolicyName=s3_bedrock_finetuning_access_policy,
        PolicyDocument=ACCESS_POLICY_DOC
    )

    policy_arn = response["Policy"]["Arn"]
    print("PolicyArn: ",policy_arn)

    ## Attaching policy to role
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn,
    )
else:
    response = iam.get_role(RoleName=role_name)
    role_arn = response["Role"]["Arn"]

jobname = "RNS-Haiku-Finetuning-Job-10"

## HyperParameters to use for Claude models: https://docs.aws.amazon.com/bedrock/latest/userguide/cm-hp-anth-claude-3.html
## In our case, we leave learningRateMultiplier as default

response = br_cl.create_model_customization_job(
            jobName = jobname,
            customModelName = "RNS-Owned-Haiku-Model",
            roleArn = role_arn,
            baseModelIdentifier = "anthropic.claude-3-haiku-20240307-v1:0:200k",
            customizationType = "FINE_TUNING",
            trainingDataConfig = {
                    "s3Uri": "s3://rns-bedrock-documents/case-4-qna/",
                },
            outputDataConfig = {
                "s3Uri": "s3://rns-bedrock-documents/output_data/"
                },
            hyperParameters = {
                "epochCount": "10",
                "batchSize": "32",
                }
        )

status = br_cl.get_model_customization_job(jobIdentifier=jobname)["status"]

while status == "InProgress":
    print("Status of the finetuning job, ", jobname, " is ", status)
    time.sleep(10)
    status = br_cl.get_model_customization_job(jobIdentifier=jobname)["status"]
