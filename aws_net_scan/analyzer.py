import botocore
from .entities import AwsObjectData
from .aws_services_data import AwsServicesData
from .logger import Logger
from .services import AwsService
from .utils import *


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
                tags = None
                name = ''
                if 'Tags' in vpc:
                    tags = vpc['Tags']
                    name = self.get_service_name(vpc['Tags'])
                self.data.add_vpc(
                    AwsObjectData(
                        vpc_id=vpc['VpcId'],
                        self_id=vpc['VpcId'],
                        cidr=vpc['CidrBlock'],
                        tags=tags,
                        igw=igw,
                        name=name
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

        self.__search_rds()

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
                tags = None
                name = ''
                if 'Tags' in subnet:
                    tags = subnet['Tags']
                    name = self.get_service_name(subnet['Tags'])
                self.data.add_subnet(
                    AwsObjectData(
                        self_id=subnet['SubnetId'],
                        vpc_id=vpc.vpc_id,
                        tags=tags,
                        cidr=subnet['CidrBlock'],
                        route_tables=route_tables,
                        name=name
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
            for ec2 in ec2s['Reservations']:
                for instance in ec2['Instances']:
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

    def __search_rds(self):
        try:
            response = self.aws_service.get_rds_instances()
            for db_instance in response['DBInstances']:
                if 'DBSubnetGroup' in db_instance:
                    if 'Subnets' in db_instance['DBSubnetGroup']:
                        for rds_subnet in db_instance['DBSubnetGroup']['Subnets']:
                            for subnet in self.data.subnets:
                                if rds_subnet['SubnetIdentifier'] == subnet.id:
                                    self.data.add_rds(
                                        AwsObjectData(
                                            self_id=db_instance['DBInstanceIdentifier'],
                                            subnet_id=subnet.id,
                                            vpc_id=db_instance['DBSubnetGroup']['VpcId'],
                                            name=db_instance['DBInstanceIdentifier'],
                                            engine=db_instance['Engine']
                                        )
                                    )

            response_clusters = self.aws_service.get_rds_clusters()
            cluster_subnet_groups = {}
            cluster_subnet_engine = {}
            for cluster in response_clusters['DBClusters']:
                cluster_subnet_groups[cluster['DBSubnetGroup']] = cluster['DBClusterIdentifier']
                cluster_subnet_engine[cluster['DBSubnetGroup']] = cluster['Engine'] + ' ' + cluster['EngineMode']

            response_subnets = self.aws_service.get_subnets_from_db_group()
            for subnet_group in response_subnets['DBSubnetGroups']:
                if subnet_group['DBSubnetGroupName'] in cluster_subnet_groups.keys():
                    subnets_visited = []
                    for subnet in subnet_group['Subnets']:
                        if not subnet['SubnetIdentifier'] in subnets_visited:
                            self.data.add_rds(
                                AwsObjectData(
                                    self_id=cluster_subnet_groups[subnet_group['DBSubnetGroupName']],
                                    subnet_id=subnet['SubnetIdentifier'],
                                    engine=cluster_subnet_engine[subnet_group['DBSubnetGroupName']]
                                )
                            )
                            subnets_visited.append(subnet['SubnetIdentifier'])
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting rds.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS to get subnets. '
                                    'Try in a few minutes.', e)