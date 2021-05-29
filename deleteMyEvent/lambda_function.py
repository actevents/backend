import json
import boto3

def lambda_handler(event, context):
    #get parameters out of pathParameters
    parameters = event["pathParameters"]
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Events")
    #try to get user
    try:
        user = event["requestContext"]["authorizer"]["claims"]
        email = user["email"]
    except Exception as inst:
        print("")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error getting the user of request\n\n" + str(type(inst)) + "\n\n" + str(inst.args))
        }
    #try to get id of parameters
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
    
    #try to delete event
    try:
        response = table.get_item(Key={"id":id})
        item = response["Item"]
        if not item["organizer"] == email:
            return {
                "statusCode": 403,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": "You cant delete the event, because you are not the organizer of the event!"
            }
        else:
            table.delete_item(Key={"id":id})
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps("The event is successfully deleted.")
            }
    except Exception as ex:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: Error getting event by id\n" + str(type(ex)) + "\n\n" + str(ex.args))
        }