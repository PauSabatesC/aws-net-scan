import boto3
from botocore.config import Config
from .utils import *
from .logger import Logger


class AwsService:
    def __init__(self, profile_name: str, log: Logger):
        self.log = log
        config = Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        boto3.setup_default_session(profile_name=profile_name)

        self.aws_ec2_client = boto3.client('ec2')
        self.rds_client = boto3.client('rds')
        self.elbv2_client = boto3.client('elbv2')
        self.ecs_client = boto3.client('ecs')

    def get_vpcs(self, vpc_id: str = None):
        if vpc_id:
            response = self.aws_ec2_client.describe_vpcs(VpcIds=[vpc_id])
        else:
            response = self.aws_ec2_client.describe_vpcs()

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting vpc data.')


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
            self.log.error('AWS http response error getting internet gateway data.')


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
            self.log.error('AWS http response error getting subnet data.')


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
            self.log.error('AWS http response error getting route tables data.')


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
            self.log.error('AWS http response error getting main route tables data.')


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
            self.log.error('AWS http response error getting ec2 data.')


    def get_rds_instances(self):
        response = self.rds_client.describe_db_instances()

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting rds intances data.')


    def get_rds_clusters(self):
        response = self.rds_client.describe_db_clusters()

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting rds clusters data.')


    def get_subnets_from_db_group(self):
        response = self.rds_client.describe_db_subnet_groups()

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting subnets of rds data.')


    def get_elbs(self):
        response = self.elbv2_client.describe_load_balancers()

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting elb data.')


    def get_ecs_tasks_data(self, tasks_arn: list, cluster: str):
        response = self.ecs_client.describe_tasks(
            tasks=tasks_arn,
            cluster=cluster
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting ecs tasks data.')


    def get_ecs_tasks_list(self, cluster_arn: str):
        response = self.ecs_client.list_tasks(cluster=cluster_arn)

        if validate_aws_response(response):
            return response['taskArns']
        else:
            self.log.error('AWS http response error getting tasks list.')


    def get_ecs_clusters(self):
        response = self.ecs_client.list_clusters()

        if validate_aws_response(response):
            return response['clusterArns']
        else:
            self.log.error('AWS http response error getting ecs clusters data.')


    def get_network_interface_public_ip(self, private_ip: str):
        response = self.aws_ec2_client.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'addresses.private-ip-address',
                    'Values': [
                        private_ip
                    ]
                }
            ]
        )

        if validate_aws_response(response):
            return response
        else:
            self.log.error('AWS http response error getting network interface data.')
