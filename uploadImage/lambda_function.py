import json
import boto3
import uuid

def lambda_handler(event, context):
    id = uuid.uuid4()
    
    table = boto3.resource('dynamodb')
    parameters = event["queryStringParameters"]
    contentType = parameters["extension"]
    bucket = "acteventsimages"
    s3 = boto3.client('s3')
    
    if contentType == 'jpeg' or contentType == 'jpg' or contentType == 'jpe':
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket':  bucket,
                'Key': str(id) + '.jpg',
                'ContentType': 'image/jpeg'
            }
        )
        fileName = str(id) + '.jpg'
    elif contentType == 'png':
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket':  bucket,
                'Key': str(id) + '.png',
                'ContentType': 'image/png'
            }
        )
        fileName = str(id) + '.png'
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Error: Wrong extension given. Extension must be jpeg jpg jpe or png")
        }
    
    item = {'uploadUrl': url,
        'fileName': fileName
    }
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*"
            },
        "body": json.dumps(item)
    }
