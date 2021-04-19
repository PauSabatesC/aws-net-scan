class AwsObjectData:
    """
    POCO entity class for storing aws service data.
    """

    def __init__(self, self_id: str, vpc_id: str, tags: list = None, name: str = None):
        self.id = self_id
        self.vpc_id = vpc_id
        self.tags = tags
        self.name = name


class AwsCredentials:
    """
    Credentials of aws user running script.
    """

    def __init__(self, profile, aws_key, aws_access_key, region):
        self.profile = profile
        self.aws_key = aws_key
        self.aws_access_key = aws_access_key
        self.region = region
