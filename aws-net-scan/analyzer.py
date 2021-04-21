import botocore
from entities import AwsObjectData
from aws_services_data import AwsServicesData
from logger import Logger
from services import AwsService
import utils


class Analyzer:
    def __init__(self, services_data: AwsServicesData, log: Logger, aws_service: AwsService):
        self.log = log
        self.data = services_data
        self.aws_service = aws_service

    def get_service_name(self, tags: list) -> str:
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']
        return ''

    def search_vpcs(self, vpc_id=None):
        try:
            if vpc_id:
                vpcs = self.aws_service.get_vpcs(vpc_id)
            else:
                vpcs = self.aws_service.get_vpcs()

            for vpc in vpcs['Vpcs']:
                inetgws = self.aws_service.get_inet_gateways(vpc['VpcId'])
                igw = 'None'
                if len(inetgws['InternetGateways']) > 0:
                    igw = inetgws['InternetGateways'][0]['InternetGatewayId']

                self.data.add_vpc(
                    AwsObjectData(
                        vpc_id=vpc['VpcId'],
                        self_id=vpc['VpcId'],
                        cidr=vpc['CidrBlock'],
                        tags=vpc['Tags'],
                        igw=igw,
                        name=self.get_service_name(vpc['Tags'])
                    )
                )
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting vpc data from AWS.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS to get VPCs. Try in a few minutes.', e)

    def scan_services(self):
        for vpc in self.data.vpcs:
            self.__search_subnets(vpc)
        for subnet in self.data.subnets:
            self.__search_ec2(subnet)

    def __search_subnets(self, vpc: AwsObjectData):
        try:
            subnets = self.aws_service.get_subnets(vpc.vpc_id)
            for subnet in subnets['Subnets']:
                route_tables_res = self.aws_service.get_route_tables(subnet['SubnetId'])
                if len(route_tables_res['RouteTables']) > 0:
                    route_tables = route_tables_res['RouteTables'][0]['Routes']
                else:  # The subnet has no route table attached, so it'll use the main VPC route table
                    response = self.aws_service.get_route_tables_main_vpc(vpc.vpc_id)
                    route_tables = response['RouteTables'][0]['Routes']
                self.data.add_subnet(
                    AwsObjectData(
                        self_id=subnet['SubnetId'],
                        vpc_id=vpc.vpc_id,
                        tags=subnet['Tags'],
                        cidr=subnet['CidrBlock'],
                        route_tables=route_tables,
                        name=self.get_service_name(subnet['Tags'])
                    )
                )
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting subnets from VPC.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS to get subnets. '
                                    'Try in a few minutes.', e)

    def __search_ec2(self, subnet):
        try:
            ec2s = self.aws_service.get_ec2s(subnet.id)
            for ec2 in ec2s:
                for reservation in ec2s['Reservations']:
                    for instance in reservation['Instances']:
                        tags = None
                        name = ''
                        if 'Tags' in instance:
                            tags = instance['Tags']
                            name = self.get_service_name(instance['Tags'])
                        public_ip = ''
                        if 'PublicIpAddress' in instance:
                            public_ip = instance['PublicIpAddress']

                        self.data.add_ec2(
                            AwsObjectData(
                                self_id=instance['InstanceId'],
                                subnet_id=subnet.id,
                                vpc_id=subnet.vpc_id,
                                tags=tags,
                                name=name,
                                public_ip=public_ip,
                                private_ip=instance['PrivateIpAddress'],
                                sec_groups=instance['SecurityGroups'],
                                instance_type=instance['InstanceType'],
                                state=instance['State']['Name']
                            )
                        )
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting subnets from VPC.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS to get ec2s. Try in a few minutes.', e)
