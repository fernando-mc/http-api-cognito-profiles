import json


def request_not_authorized_response():
    return {
        'statusCode': 403,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps('Not authorized')
    }


def success_response(response):
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(response)
    }
