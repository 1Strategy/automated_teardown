import boto3


def lambda_handler(event, context):

    dry_run = True if event.get('dry_run') is None else event['dry_run']

    if event.get('protected_resources') is None:
        protected_resources = ['default']
    else:
        protected_resources = event['protected_resources']

    ec2_client = boto3.client('ec2', region_name=event['region'])
    security_groups = ec2_client.describe_security_groups()['SecurityGroups']

    for group in security_groups:
        print(group['GroupName'])
        try:
            if group['GroupName'] not in protected_resources:
                print(
                    "Termination Succeeded: {}".format(group['GroupName'])
                )
                ec2_client.delete_security_group(DryRun=dry_run,
                                                 GroupId=group['GroupId'])
        except Exception as e:
            print("Termination Failed: {error}".format(error=e))

    return event
event = {
            'protected_resources': {
                'EC2': ['default',
                        'ElasticMap',
                        'bastion-ssh',
                        'RDP Access',
                        'redshift-connect',
                        'rds-launch-wizard',
                        'ElasticMapReduce-master',
                        'ElasticMapReduce-slave'
                        ],
                'a': 'b'
            },
            'dry_run': True
        }

lambda_handler(event, {})
