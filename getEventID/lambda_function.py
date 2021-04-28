import json
import boto3

#getEventID
def lambda_handler(event, context):
    #get body out of event
    bodyStr = event["body"].replace("\\n", "")
    body = json.loads(bodyStr)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    try:
        id = str(body['id'])
    except:
        return {
            "statusCode": 400,
            "body": json.dumps("Error: Could not get id as parameter.")
        }
    try:
        response = table.get_item(Key={'id':id})
        item = response['Item']
        return {
            'statusCode': 200,
            'body': item
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Error getting events by id')
        }
