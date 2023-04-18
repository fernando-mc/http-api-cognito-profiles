import boto3
from cognito_auth import authorize_request, authorize_request_undecorated
from boilerplate_responses import (
    request_not_authorized_response, success_response
)
import os
import json

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(TABLE_NAME)


def create(event, context):
    # Two line authorization without using a decorator
    if not authorize_request_undecorated(event, ['user']):
        return request_not_authorized_response()
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
    return success_response(item)


@authorize_request(['user'])
def get(event, context):
    user_sub = event['requestContext']['authorizer']['claims']['sub']
    try:
        item = table.get_item(
            Key={
                'pk': 'USERS#ALL',
                'sk': 'USER#' + user_sub
            }
        )['Item']
        return success_response(item)
    except KeyError:
        return success_response({})


@authorize_request(['admin'])
def get_all(event, context):
    try:
        items = table.query(
            KeyConditionExpression='pk = :pk AND begins_with(sk, :sk)',
            ExpressionAttributeValues={
                ':pk': 'USERS#ALL',
                ':sk': 'USER#'
            }
        )['Items']
        return success_response(items)
    except KeyError:
        return success_response({})
