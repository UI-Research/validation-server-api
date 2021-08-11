import boto3
import json
import os

def trigger_smartnoise(instance, confidential_query=False):
    # pull fields and create lambda payload
    command_id = getattr(instance, "command_id").command_id
    command = Command.objects.get(command_id=command_id)
    payload = {
        "command_id": command_id,
        "run_id": instance.run_id,
        "confidential_query": confidential_query,
        "epsilon": instance.epsilon,
        "transformation_query": command.sanitized_command_input["transformation_query"],
        "analysis_query": command.sanitized_command_input["analysis_query"],
        "debug": os.getenv("SMARTNOISE_DEBUG", True)
    }
    payload = json.dumps(payload).encode()
    # invoke lambda function
    client = boto3.client(
        "lambda", 
        region_name="us-east-1",
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    response = client.invoke(
        FunctionName="validation-server-engine", 
        InvocationType="Event", 
        Payload=payload
    )