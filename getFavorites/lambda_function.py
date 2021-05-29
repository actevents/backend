import json
import boto3

def lambda_handler(event, context):
    #create connection for database
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Favorites")
    tableEvents = dynamodb.Table("Events")

    #get user
    user = event["requestContext"]["authorizer"]["claims"]
    # user = {"email": "test@test.de"}
    userId = user["email"]
    favorites = list()

    response = table.get_item(Key={"user": userId})
    if "Item" in response:
        for item in response["Item"]["favorites"]:
            try:
                favorites.append(tableEvents.get_item(Key={"id":item})["Item"])
            except Exception as ex:
                #event is probably deleted or not in database
                print(ex)
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(favorites)
        }
    else:
        item = {
            "user": userId,
            "favorites": favorites
        }
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(item)
        }
