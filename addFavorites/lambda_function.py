import json
import boto3

def lambda_handler(event, context):
    #create connection for database
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Favorites")

    #get user
    user = event["requestContext"]["authorizer"]["claims"]
    userId = user["email"]
    favorites = list()
    try:
        parameter = event["queryStringParameters"]
        newFavorite = parameter["favorite"]
    except Exception as ex:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: Could not get parameter.\n" + str(type(ex)) + "\n\n" + str(ex.args))
        }
    favorites.append(newFavorite)

    try:
        response = table.get_item(Key={"user": userId})
        if "Item" in response:
            for item in response["Item"]["favorites"]:
                if item != newFavorite:
                    favorites.append(item)
            table.update_item(
                Key={
                    "user": userId
                },
                UpdateExpression="set favorites=:f",
                ExpressionAttributeValues={
                    ":f": favorites
                }
            )
        else:
            table.put_item(
                Item={
                    "user": userId,
                    "favorites": favorites
                }
            )
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps("Sucessfull added new favorite")
        }
    except Exception as ex:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: Could not update or create favorites for the user\n" + str(type(ex)) + "\n\n" + str(ex.args))
        }
