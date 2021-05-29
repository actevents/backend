import json
import boto3
import uuid
import datetime

#createEvent
def lambda_handler(event, context):
    #get body out of event
    try:
        #bodyStr = event["body"].replace("\\n", "")
        bodyStr = event["body"]
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
        if "fileName" in body:
            fileName = body["fileName"]
        else:
            fileName = ""
    except Exception as ex:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error getting parameters from client\n\n" + str(type(ex)) + "\n\n" + str(ex.args))
        }
    try:
        #check if end date is after begin date
        datesBeginObj = datetime.datetime.strptime(datesBegin, "%Y-%m-%dT%H:%M:%S.%fZ")
        datesEndObj = datetime.datetime.strptime(datesEnd, "%Y-%m-%dT%H:%M:%S.%fZ")
        if not datesEndObj > datesBeginObj:
            return {
                "statusCode": 406,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps("Error: End date is not after begin date")
            }
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
                "tags": tags,
                "image": fileName
            }
        )
    except Exception as inst:
        print("Closing lambda function")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error saving the event\n\n" + str(type(inst)) + "\n\n" + str(inst.args))
        }
        
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps("Event created successfully")
    }