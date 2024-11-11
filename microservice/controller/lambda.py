import boto3
import json

ecs_client = boto3.client('ecs')

def lambda_handler(event, context):
    source = event.get('source')
    if source == "EventBridge":
        task_payload = {
            "source": "EventBridge",
            "records": get_batch_records_from_rds()
        }
    elif source == "API Gateway":
        user_record = get_single_record_from_payload(event)
        task_payload = {
            "source": "API Gateway",
            "record": user_record
        }

    response = ecs_client.run_task(
        cluster='your-ecs-cluster',
        taskDefinition='your-task-definition',
        launchType='FARGATE',
        overrides={
            'containerOverrides': [
                {
                    'name': 'your-container-name',
                    'environment': [{'name': 'PAYLOAD', 'value': json.dumps(task_payload)}]
                }
            ]
        },
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-abc123'],
                'securityGroups': ['sg-123456'],
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    return response
