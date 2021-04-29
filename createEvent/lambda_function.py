import json
import boto3
import uuid

#createEvent
def lambda_handler(event, context):
    #get body out of event
    bodyStr = event["body"].replace("\\n", "")
    body = json.loads(bodyStr)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    acteventID = uuid.uuid4()
    acteventName = body['name']
    acteventLongitude = body['longitude']
    acteventLatitude = body['latitude']
    try:
        table.put_item(
            Item={
                'id': str(acteventID), 
                'name': acteventName,
                'longitude': acteventLongitude,
                'latitude': acteventLatitude
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps('Successfully created event!')
        }
    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps('Error saving the event')
        }