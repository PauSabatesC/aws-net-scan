import boto3
from botocore.config import Config
from .utils import *
from .logger import Logger


class AwsService:
    def __init__(self, aws_key: str, aws_secret_key: str, region: str, log: Logger):
        self.log = log
        config = Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        self.aws_ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=str(aws_key),
            aws_secret_access_key=str(aws_secret_key),
            region_name=str(region),
            config=config
        )

    def get_vpcs(self, vpc_id: str = None):
        if vpc_id:
            response = self.aws_ec2_client.describe_vpcs(VpcIds=[vpc_id])
        else:
            response = self.aws_ec2_client.describe_vpcs()

        if validate_aws_response(response):
            return response
        else:
            self.log.error_and_exit('AWS http response error getting vpc data.')

    def get_inet_gateways(self, vpc_id):
        response = self.aws_ec2_client.describe_internet_gateways(
            Filters=[
                {
                    'Name': 'attachment.vpc-id',
                    'Values': [
                        vpc_id
                    ]
                }
            ]
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error_and_exit('AWS http response error getting internet gateway data.')

    def get_subnets(self, vpc_id):
        response = self.aws_ec2_client.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id
                    ]
                }
            ]
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error_and_exit('AWS http response error getting subnet data.')

    def get_route_tables(self, subnet_id):
        response = self.aws_ec2_client.describe_route_tables(
            Filters=[
                {
                    'Name': 'association.subnet-id',
                    'Values': [
                        subnet_id
                    ]
                }
            ]
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error_and_exit('AWS http response error getting route tables data.')

    def get_route_tables_main_vpc(self, vpc_id):
        response = self.aws_ec2_client.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id
                    ]
                },
                {
                    'Name': 'association.main',
                    'Values': [
                        'true'
                    ]
                }
            ]
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error_and_exit('AWS http response error getting main route tables data.')

    def get_ec2s(self, subnet_id):
        response = self.aws_ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'subnet-id',
                    'Values': [
                        subnet_id
                    ]
                }
            ]
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error_and_exit('AWS http response error getting main route tables data.')



