from math import cos, asin, sqrt, pi
import json
import boto3

#getAllEvents
def lambda_handler(event, context):
    #return {
    #    "body": json.dumps(event)
    #    }
    
    #get body out of event
    #bodyStr = event["body"].replace("\\n", "")
    #body = json.loads(bodyStr)
    parameters = event["queryStringParameters"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    try:
        lon = float(parameters["longitude"])
        lat = float(parameters["latitude"])
        if "radius" in parameters:
            radius =  int(parameters["radius"])
        else:
            radius = 15
    except:
        return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps("Error: Could not get parameters.")
        }
    try:
        response = table.scan()
        all_items = response['Items']
        items = []
        for item in all_items:
            distance = getDistance(lat,lon,float(item['latitude']),float(item['longitude']))
            item.update({"distance": distance})
            if(distance<=radius):
                items.append(item)
        
        items.sort(key=sortFunc)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
        }
    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps('Error getting events from db in the given radius')
    } 

def getDistance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def sortFunc(e):
    return e["distance"]