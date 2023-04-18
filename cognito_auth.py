from functools import wraps
from boilerplate_responses import request_not_authorized_response


def authorize_request_undecorated(event, required_groups: list):
    try:
        claims = event['requestContext']['authorizer']['claims']
        cognito_groups_in_event = claims['cognito:groups']
        if not set(required_groups).issubset(cognito_groups_in_event):
            return request_not_authorized_response()
    except KeyError:
        return request_not_authorized_response()


def authorize_request(required_groups: list):
    def groups_required(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                claims = event['requestContext']['authorizer']['claims']
                cognito_groups_in_event = claims['cognito:groups']
                if not set(required_groups).issubset(cognito_groups_in_event):
                    return request_not_authorized_response()
            except KeyError:
                return request_not_authorized_response()
            return func(event, context)
        return wrapper
    return groups_required
