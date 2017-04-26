import boto3


def lambda_handler(event, context):

    clusters_to_terminate = []
    instances_to_terminate = []

    emr_client = boto3.Session(profile_name='training'
                               ).client(
                                    'emr',
                                    region_name=event['region']
                                 )

    clusters = emr_client.list_clusters()['Clusters']

    # print(instances)
    for item in clusters:
        if item['Status']['State'] == 'WAITING':
            print(item['Id'])
            emr_client.set_termination_protection(JobFlowIds=[item['Id']],
                                                  TerminationProtected=False)
            emr_client.terminate_job_flows(JobFlowIds=[item['Id']])




lambda_handler({
                'region':
                'us-west-2'
               }, {})
