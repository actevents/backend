import json
import boto3

#getEventID
def lambda_handler(event, context):
    #get parameters out of queryStringParameters
    parameters = event["queryStringParameters"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    try:
        id = str(parameters['id'])
    except:
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps("Error: Could not get id as parameter.")
        }
    try:
        response = table.get_item(Key={'id':id})
        item = response['Item']
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }
    except Exception as inst:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps('Error: Error getting events by id\n' + str(type(inst)) + '\n\n' + str(inst.args))
        }
