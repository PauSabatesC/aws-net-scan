import boto3
import botocore
from entities import AwsObjectData
from aws_services_data import AwsServicesData
from logger import Logger
import utils


class Analyzer:
    def __init__(self, services_data: AwsServicesData,
                 aws_key: str, aws_secret_key: str, log: Logger):
        self.log = log
        self.data = services_data
        self.aws_session = boto3.Session(
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret_key,
            region_name=services_data.region
        )
        self.aws_ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret_key,
            region_name=services_data.region
        )
        self.aws_ec2_res = self.aws_session.resource('ec2')

    def search_vpcs(self, vpc_id=None):
        try:
            if vpc_id:
                response = self.aws_ec2_client.describe_vpcs(VpcIds=[vpc_id])
            else:
                response = self.aws_ec2_client.describe_vpcs()

            res_ok = utils.validate_aws_response(response)
            if res_ok:
                for vpc in response['Vpcs']:
                    response = self.aws_ec2_client.describe_internet_gateways(
                        Filters=[
                            {
                                'Name': 'attachment.vpc-id',
                                'Values': [
                                    vpc['VpcId']
                                ]
                            }
                        ]
                    )
                    res_ok = utils.validate_aws_response(response)
                    igw = 'None'
                    if len(response['InternetGateways']) > 0:
                        igw = response['InternetGateways'][0]['InternetGatewayId']
                    if res_ok:
                        self.data.add_vpc(
                            AwsObjectData(
                                vpc_id=vpc['VpcId'],
                                self_id=vpc['VpcId'],
                                cidr=vpc['CidrBlock'],
                                tags=vpc['Tags'],
                                igw=igw
                            )
                        )
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting vpc data from AWS.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS. Try in a few minutes.', e)

    def search_subnets(self):
        try:
            for vpc in self.data.vpcs:
                response = self.aws_ec2_client.describe_subnets(
                    Filters=[
                        {
                            'Name': 'vpc-id',
                            'Values': [
                                vpc.vpc_id
                            ]
                        }
                    ]
                )
                res_ok = utils.validate_aws_response(response)
                for subnet in response['Subnets']:
                    response = self.aws_ec2_client.describe_route_tables(
                        Filters=[
                            {
                                'Name': 'association.subnet-id',
                                'Values': [
                                    subnet['SubnetId']
                                ]
                            }
                        ]
                    )
                    res_ok = utils.validate_aws_response(response)
                    route_tables = None
                    if len(response['RouteTables']) > 0:
                        route_tables = response['RouteTables'][0]['Routes']
                    else: #The subnet has no route table attached, so it'll use the main VPC route table
                        response = self.aws_ec2_client.describe_route_tables(
                            Filters=[
                                {
                                    'Name': 'vpc-id',
                                    'Values': [
                                        vpc.vpc_id
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
                        res_ok = utils.validate_aws_response(response)
                        route_tables = response['RouteTables'][0]['Routes']
                    self.data.add_subnet(
                        AwsObjectData(
                            self_id=subnet['SubnetId'],
                            vpc_id=vpc.vpc_id,
                            tags=subnet['Tags'],
                            cidr=subnet['CidrBlock'],
                            route_tables=route_tables
                        )
                    )
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting subnets from VPC.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS. Try in a few minutes.', e)

# VPC_IDS=$(aws ec2 describe-vpcs --region eu-west-2 --filters 'Name=tag:Name,Values=pmUtilts-VPC-VPN' | grep VpcId | awk '{ print $2 }' | sed 's/[\",]//g')
