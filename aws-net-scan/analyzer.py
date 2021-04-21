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
                            route_tables=route_tables
                        )
                    )
        except botocore.exceptions.ClientError as e:
            self.log.error_and_exit('Error getting subnets from VPC.', e)
        except botocore.exceptions.EndpointConnectionError as e:
            self.log.error_and_exit('Could not be stablished a connection to AWS. Try in a few minutes.', e)
