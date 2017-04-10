import boto3

def lambda_handler(event, context):

    ec2_client = boto3.client('ec2',region_name=event['region'])
    security_groups = ec2_client.describe_security_groups()['SecurityGroups']

    protected_resource_names = ['default']

    for group in security_groups:
        try:
            if not group['GroupName'].startswith('ElasticMap') and \
                group['GroupName'] not in protected_resource_names:
                print("Termination Succeeded: {group}".format(group=group['GroupName'])
                ec2_client.delete_security_group(DryRun=False, GroupId=group['GroupId'])
        except Exception as e:
            print("Termination Failed: {error}".format(error=e))
