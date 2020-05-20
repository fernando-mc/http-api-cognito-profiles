import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(TABLE_NAME)


def create(event, context):
    print(event)
    user_sub = event['requestContext']['authorizer']['claims']['sub']
    profile_data = json.loads(event['body'])
    item = {
        'pk': 'USERS#ALL',
        'sk': 'USER#' + user_sub,
        'profile_data': profile_data
    }
    table.put_item(
        Item=item
    )
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(item)
    }


def get(event, context):
    print(event)
    user_sub = event['requestContext']['authorizer']['claims']['sub']
    pk = 'USERS#ALL'
    sk = 'USER#' + user_sub
    result = table.get_item(
        Key={
            'pk': pk,
            'sk': sk
        }
    )
    print(result)
    item_info = result['Item']
    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(item_info)
    }
    return response
