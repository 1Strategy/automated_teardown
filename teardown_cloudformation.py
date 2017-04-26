import boto3


def lambda_handler(event, context):

    # cf_client = boto3.client('cloudformation', region_name=event['region'])
    cf_client = boto3.Session(
            profile_name='sandbox'
            ).client('cloudformation', region_name=event['region'])

    stacks = cf_client.describe_stacks()['Stacks']

    for stack in stacks:
        print(stack['StackName'])
        response = cf_client.delete_stack(StackName='string')

lambda_handler({'region': 'us-west-2'}, {})
