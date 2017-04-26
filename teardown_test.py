import teardown_instances
import boto3
import json
import pprint
import datetime

session = boto3.Session()
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key
token = credentials.token
print(credentials.token)4

with open('/Users/jiravani/Desktop/instances.json') as data_file:
    instances = json.load(data_file)['Reservations']


def instance_terminate_test(ttl, protected_resources):
    for instance in instances:

        time = datetime.datetime.now() - datetime.timedelta(hours=ttl)

        instance['Instances'][0]['LaunchTime'] = time

        # instance['Instances'][0]['State']['Name'] = 'terminated'

        if teardown_instances.should_terminate(instance, protected_resources):
            print('{}'.format(
                instance['Instances'][0]['InstanceId']
                )
            )

instance_terminate_test(5, ['keepalive', 'aws:elasticmap'])


def test_1(capfd):
    instance_terminate_test(3, ['keepalive', 'Lab'])
    out, err = capfd.readouterr()
    assert out == 'i-06b17a7e7abe86a6e(EMR)\ni-06b17a7e7abe86a6e(EC2)\n'


def test_2(capfd):
    instance_terminate_test(5, ['keepalive', 'aws:elasticmap'])
    out, err = capfd.readouterr()
    assert out == 'i-06b17a7e7abe86a6e(EC2)\ni-06b17a7e7abe86a6e(Lab)\n'
