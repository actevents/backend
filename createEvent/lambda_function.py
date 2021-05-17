import json
import boto3
import uuid

#createEvent
def lambda_handler(event, context):
    #get body out of event
    bodyStr = event["body"].replace("\\n", "")
    body = json.loads(bodyStr)
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Events")
    id = uuid.uuid4()
    name = body["name"]
    description = body["description"]
    user = event["requestContext"]["authorizer"]["claims"]
    organizer = user["email"]
    price = body["price"]
    locLatitude = body["location"]["longitude"]
    locLongitude = body["location"]["latitude"]
    datesBegin = body["dates"]["begin"]
    datesEnd = body["dates"]["end"]
    tags = body["tags"]

    try:
        table.put_item(
            Item={
                "id": str(id), 
                "name": name,
                "description": description,
                "organizer": organizer,
                "price": price,
                "location": {
                    "longitude": locLatitude,
                    "latitude": locLongitude
                },
                "dates": {
                    "begin": datesBegin,
                    "end": datesEnd
                },
                "tags": tags

            }
        )
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Successfully created event!")
        }
    except Exception as inst:
        print("Closing lambda function")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error saving the event\n\n" + str(type(inst)) + "\n\n" + str(inst.args))
        }