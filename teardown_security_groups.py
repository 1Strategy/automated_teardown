import boto3


def lambda_handler(event, context):

    dry_run = True if 'dry_run' not in event else event['dry_run']

    protected_resources = ['default'] if 'protected_resources' not in event else event['protected_resources']
    print(protected_resources)
    print(dry_run)
    return

    # ec2_client = boto3.client('ec2', region_name=event['region'])
    security_groups = ec2_client.describe_security_groups()['SecurityGroups']

    for group in security_groups:
        print(group['GroupName'])
        try:
            if group['GroupName'] not in protected_resources:
                print(
                    "Termination Succeeded: {group}".format(group=group['GroupName'])
                )
                ec2_client.delete_security_group(DryRun=dry_run,
                                                 GroupId=group['GroupId'])
        except Exception as e:
            print("Termination Failed: {error}".format(error=e))

event = {
    'protected_resources': ['default',
                            'ElasticMap',
                            'bastion-ssh',
                            'RDP Access',
                            'redshift-connect',
                            'rds-launch-wizard',
                            'ElasticMapReduce-master',
                            'ElasticMapReduce-slave'
                            ],
    'dry_run': True
}

lambda_handler(event, {})
