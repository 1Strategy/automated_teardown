import boto3
from datetime import datetime
from datetime import timedelta


def lambda_handler(event, context):

    rds_client = boto3.client('rds', region_name=event['region'])

    for instance in rds_client.describe_db_instances()['DBInstances']:

        create_time = instance['InstanceCreateTime'].tzinfo
        now = datetime.now(create_time)
        db_instance = instance['DBInstanceIdentifier']

        if now-create_time > timedelta(hours=2):
            try:
                print("Terminating RDS instance: {}".format(db_instance))

                rds_client.delete_db_instance(DBInstanceIdentifier=db_instance,
                                              SkipFinalSnapshot=True)

                print("{} successfully destroyed".format(db_instance))
            except Exception as e:
                print("Unable to delete database intance {db}: {error}".format(db=db_instance,
                                                                               error=e))
