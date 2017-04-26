import boto3


def lambda_handler(event, context):
    redshift_client = boto3.Session(profile_name='training'
                                    ).client(
                                    'redshift',
                                    region_name=event['region']
                                 )


    clusters = redshift_client.describe_clusters()['Clusters']
    print(clusters)
    for cluster in clusters:
        if 'agrvs' not in cluster['ClusterIdentifier']:
            print(cluster['ClusterIdentifier'])
            redshift_client.delete_cluster(ClusterIdentifier=cluster['ClusterIdentifier'],
                                           SkipFinalClusterSnapshot=True)

lambda_handler({'region': 'us-west-2'}, {})
