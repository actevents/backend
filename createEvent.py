import json
import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    acteventID = uuid.uuid4()
    bodyStr = event["body"].replace("\\n", "")
    body = json.loads(bodyStr)
    acteventName = body['name']
    try:
        table.put_item(
            Item={
                'id': str(acteventID), 
                'name': acteventName 
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully created event!')
        }
    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps('Error saving the event')
        }