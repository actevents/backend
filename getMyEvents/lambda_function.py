import json
import boto3

#getMyEvents
def lambda_handler(event, context):
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

    #search in db for email as organiser
    try:
        response = table.scan()
        all_items = response["Items"]
        items = []
        for item in all_items:
            try:
                if item["organizer"] == email:
                    items.append(item)
            except:
                items.append(item)
        return {
            'statusCode': 200,
            "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
            'body': json.dumps(items)
        }
    except Exception as inst:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error getting events from db with given user as organizer\n\n" + str(type(inst)) + "\n\n" + str(inst.args))
    }
