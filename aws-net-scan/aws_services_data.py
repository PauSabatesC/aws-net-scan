from typing import List
from entities import AwsObjectData
from logger import Logger
from printer import *

class AwsServicesData:
    """
    Lists of different aws services data.
    """
    def __init__(self, aws_region: str, log: Logger):
        self.log = log
        self.region: str = aws_region
        self.__vpcs: List[AwsObjectData] = []
        self.__subnets: List[AwsObjectData] = []
        self.__ec2: List[AwsObjectData] = []
        self.__ecs: List[AwsObjectData] = []

    @property
    def vpcs(self) -> List[AwsObjectData]:
        return self.__vpcs

    @property
    def subnets(self) -> List[AwsObjectData]:
        return self.__subnets

    @property
    def ec2(self) -> List[AwsObjectData]:
        return self.__ec2

    @property
    def ecs(self) -> List[AwsObjectData]:
        return self.__ecs

    def add_vpc(self, vpc_data: AwsObjectData):
        if type(vpc_data) is AwsObjectData:
            self.__vpcs.append(vpc_data)

    def add_subnet(self, subnet_data: AwsObjectData):
        if type(subnet_data) is AwsObjectData:
            self.__subnets.append(subnet_data)

    def add_ec2(self, ec2_data: AwsObjectData):
        if type(ec2_data) is AwsObjectData:
            self.__ec2.append(ec2_data)

    def add_ecs(self, ecs_data: AwsObjectData):
        if type(ecs_data) is AwsObjectData:
            self.__ecs.append(ecs_data)

    def print(self):
        for vpc in self.__vpcs:
            print_vpc_data(vpc)
            for subnet in self.__subnets:
                if subnet.vpc_id == vpc.vpc_id:
                    print_subnet_data(subnet)
                    for ec2 in self.__ec2:
                        if subnet.id == ec2.subnet_id:
                            print_ec2s(ec2)

