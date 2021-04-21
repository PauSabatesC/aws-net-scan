import json


def pretty_json(dictionary: dict):
    """
    Returns a dictionary or dictionary list sorted and idented for better visualization.
    """
    return json.dumps(dictionary, indent=2, sort_keys=True, default=str)


def validate_aws_response(response: dict):
    """
    Validates if the aws http response parameter is empty or != 200.
    """
    if not response or response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False
    else:
        return True
