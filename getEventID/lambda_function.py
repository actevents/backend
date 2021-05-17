import json
import boto3

#getEventID
def lambda_handler(event, context):
    #get parameters out of pathParameters
    parameters = event["pathParameters"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Events")
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
        # if not item["organizer"] == email:
        #     return {
        #         "statusCode": 400,
        #         "headers": {
        #             "Access-Control-Allow-Origin": "*"
        #         },
        #         "body": "You are not the organizer of the event!"
        #     }
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
