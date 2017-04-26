import boto3


def lambda_handler(event, context):
    datapipeline_client = boto3.Session(profile_name='training'
                                        ).client(
                                            'datapipeline',
                                            region_name=event.get('region',
                                                                  'us-west-2')
                                        )
    pipelines = datapipeline_client.list_pipelines()['pipelineIdList']

    for pipeline in pipelines:
        if 'agrvs' not in pipeline.get('name'):
            print(pipeline.get('name'))
            response = datapipeline_client.delete_pipeline(pipelineId=pipeline.get('id'))


if __name__ == '__main__':
    lambda_handler({}, {})
