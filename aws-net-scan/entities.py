class AwsObjectData:
    """
    POCO entity class for storing aws service data.
    """

    def __init__(self, self_id: str, vpc_id: str, cidr: str=None, tags: list = None, name: str = None, **kwargs):
        self.__dict__.update(kwargs)
        self.id = self_id
        self.vpc_id = vpc_id
        self.cidr = cidr
        self.tags = tags
        self.name = name


class AwsCredentials:
    """
    Credentials of aws user running script.
    """

    def __init__(self, profile, aws_key, aws_secret_key, region):
        self.profile = profile
        self.aws_key = aws_key
        self.aws_secret_key = aws_secret_key
        self.region = region
