import boto3
import datetime

# Dry run flag for testing purposes
dry_run = True
ec2_client = []


def lambda_handler(event, context):

    # Get DryRun flag from event context
    global dry_run
    dry_run = event['dry_run']

    # Initialize/reinitialize global ec2_client
    # global ec2_client
    # ec2_client = boto3.client('ec2', region_name=event['region'])

    # Retreives a list of all of the ec2 instances in the given 'region'
    instances = ec2_client.describe_instances()['Reservations']

    # Initial the array for instances to be terminated
    instances_to_terminate = []

    # For each instance in the list of instances,
    for instance in instances:
        # determinate if they should be terminated or not.
        if should_terminate(instance):
            # add items to be terminated to the instances_to_terminate array
            # for later handling
            instances_to_terminate.append(
                instance['Instances'][0]['InstanceId']
            )

    terminate_instances(instances_to_terminate)


# Delete all the volumes identified as no longer needed
def terminate_volumes(volumes):

    for volume in volumes:
        try:
            ec2_client.delete_volume(DryRun=dry_run, VolumeId=volume)
        except Exception as e:
            print (e)


# Delete all the instances identified as no longer needed
def terminate_instances(instances):

    for instance in instances:
        try:
            # Turn off EC2 Termination protection if it's on
            ec2_client.modify_instance_attribute(DryRun=dry_run,
                                                 InstanceId=instance,
                                                 DisableApiTermination={
                                                    'Value': False
                                                 })
        except Exception as e:
            print (
                'Termination protection not active: {error}'''.format(error=e)
            )

        try:
            print(
                'Terminating instance: {instance}'.format(instance=instance)
            )
            ec2_client.terminate_instances(DryRun=dry_run,
                                           InstanceIds=[instance])

        except Exception as e:
            print ("Error terminating instance {error}".format(error=e))


# This function determines if a given instance should be terminated at runtime
def should_terminate(instance):

    # Determine when the instance was created
    launch_time = instance['Instances'][0]['LaunchTime']

    # Determines the 'state' of the instance (terminated,
    # running, stopped, etc).
    state = instance['Instances'][0]['State']

    # Creates a datetime objection with the value of the current time
    now = datetime.datetime.now(launch_time.tzinfo)

    # Default time to live is 2 hours
    ttl = 2

    # If this instance has already been terminated, no further actions need to
    # be taken
    if 'terminated' in state.get('Name'):
        return False

    # Inspect all of the tags on an instance
    if 'Tags' in instance['Instances'][0]:
        tags = instance['Instances'][0]['Tags']

        for tag in tags:

            # If an instance has a 'keepalive' tag, don't terminate it
            if 'keepalive' in tag.get('Key'):
                return False

            if 'aws:elastic' in tag.get('Key'):
                return False

            if 'Lab' in tag.get('Key'):
                return False

    # If the instance has been running for longer than permitted based on it's
    # tags hours, terminate it
    if now-launch_time > datetime.timedelta(hours=ttl):

        return True
    return False

# ec2_client = boto3.Session(profile_name='sandbox').client('ec2')
#
# lambda_handler({'region': 'us-west-2', 'dry_run': True}, {})
