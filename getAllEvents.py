import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    try:
        response = table.scan()
        items = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps('Error getting all events from db')
        }