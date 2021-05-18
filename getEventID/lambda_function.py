import json
import boto3
from math import cos, asin, sqrt, pi

#getEventID
def lambda_handler(event, context):
    #get parameters out of pathParameters
    parameters = event["pathParameters"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Events")
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
    #try to get location
    try:
        parameters = event["queryStringParameters"]
        lon = float(parameters["longitude"])
        lat = float(parameters["latitude"])
        hasLocation = True
    except KeyError:
        hasLocation = False
        print("no location given")
    #try to get item
    try:
        response = table.get_item(Key={"id":id})
        item = response["Item"]
        if hasLocation:
            try:
                distance = getDistance(lat,lon,float(item["location"]["latitude"]),float(item["location"]["longitude"]))
                item.update({"distance": distance})
            except Exception as inst:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps("Error calculating the distance\n\n" + str(type(inst)) + "\n\n" + str(inst.args))
                }
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

def getDistance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...