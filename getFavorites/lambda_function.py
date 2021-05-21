import json
import boto3

def lambda_handler(event, context):
    #create connection for database
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Favorites")

    #get user
    user = event["requestContext"]["authorizer"]["claims"]
    # user = {"email": "test@test.de"}
    userId = user["email"]

    response = table.get_item(Key={"user": userId})
    if "Item" in response:
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(response["Item"])
        }
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: The user has no favorites")
        }
