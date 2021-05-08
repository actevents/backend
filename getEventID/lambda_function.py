import json
import boto3

#getEventID
def lambda_handler(event, context):
    #get parameters out of pathParameters
    parameters = event["pathParameters"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Events")
    try:
        id = str(parameters["id"])
    except Exception as ex:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: Could not get id as parameter.\n" + str(type(ex)) + "\n\n" + str(ex.args))
        }
    try:
        response = table.get_item(Key={"id":id})
        item = response["Item"]
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(item)
        }
    except Exception as ex:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: Error getting events by id\n" + str(type(ex)) + "\n\n" + str(ex.args))
        }
