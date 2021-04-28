from math import cos, asin, sqrt, pi
import json
import boto3

def lambda_handler(event, context):
    #get body out of event
    bodyStr = event["body"].replace("\\n", "")
    body = json.loads(bodyStr)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Events')
    try:
        lon = float(body['longitude'])
        lat = float(body['latitude'])
        radius = int(body['radius'])
        
        response = table.scan()
        all_items = response['Items']
        items = []
        for item in all_items:
            distance = getDistance(lat,lon,float(item['latitude']),float(item['longitude']))
            if(distance<=radius):
                items.append([item, distance])
        
        items.sort(key=sortFunc)
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except:
        print('Closing lambda function')
        return {
            'statusCode': 400,
            'body': json.dumps('Error getting all events from db')
    } 

def getDistance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def sortFunc(e):
    return e[1]