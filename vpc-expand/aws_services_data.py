from typing import List
from entities import AwsObjectData


class AwsServicesData:
    """
    Lists of different aws services data.
    """
    def __init__(self, aws_region: str):
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
            print(vpc.name)

