import boto3
import datetime


def lambda_handler(event, context):

    rds_client = boto3.client('rds', region_name = event['region'])

    for instance in rds_client.describe_db_instances()['DBInstances']:

        if datetime.datetime.now(instance['InstanceCreateTime'].tzinfo)-instance['InstanceCreateTime'] > datetime.timedelta(hours=2):
            try:
                print("Terminating RDS instance {instance}: ".format(instance=instance['DBInstanceIdentifier']))
                rds_client.delete_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'],
                                              SkipFinalSnapshot=True)
                print("{instance} successfully destroyed".format(instance=instance['DBInstanceIdentifier']))
            except Exception as e:
                print("Unable to delete database intance {db}: {error}".format(db=instance['DBInstanceIdentifier'], error=e))
