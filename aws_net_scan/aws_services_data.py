from typing import List
from .logger import Logger
from .printer import *


class AwsServicesData:
    """
    Lists of different aws services data.
    """

    def __init__(self, log: Logger):
        self.log = log
        self.__vpcs: List[AwsObjectData] = []
        self.__subnets: List[AwsObjectData] = []
        self.__ec2: List[AwsObjectData] = []
        self.__ecs: List[AwsObjectData] = []
        self.__rds: List[AwsObjectData] = []
        self.__elb: List[AwsObjectData] = []

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

    @property
    def rds(self) -> List[AwsObjectData]:
        return self.__rds

    @property
    def elb(self) -> List[AwsObjectData]:
        return self.__elb

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

    def add_rds(self, rds_data: AwsObjectData):
        if type(rds_data) is AwsObjectData:
            self.__rds.append(rds_data)

    def add_elb(self, elb_data: AwsObjectData):
        if type(elb_data) is AwsObjectData:
            self.__elb.append(elb_data)

    def print(self):
        for vpc in self.__vpcs:
            print_vpc_data(vpc)
            # Printing all the subnets in this vpc
            for i, subnet in enumerate(self.__subnets):
                if subnet.vpc_id == vpc.vpc_id:
                    print_subnet_data(subnet)

                    # Getting all the ec2 in this subnet into a list for printing later as a table
                    ec2_list = []
                    for j, ec2 in enumerate(self.__ec2):
                        if subnet.id == ec2.subnet_id:
                            # Storing running ec2 at the start of the list
                            if ec2.state == 'running':
                                ec2_list.insert(0,ec2)
                            else:
                                ec2_list.append(ec2)
                    add_print_ec2s(ec2_list)

                    rds_list = []
                    for j, rds in enumerate(self.__rds):
                        if subnet.id == rds.subnet_id:
                            rds_list.append(rds)
                    add_print_rds(rds_list)

                    elb_list = []
                    for j, elb in enumerate(self.__elb):
                        if subnet.id == elb.subnet_id:
                            elb_list.append(elb)
                    add_print_elb(elb_list)

                    ecs_list = []
                    for j, ecs in enumerate(self.__ecs):
                        if subnet.id == ecs.subnet_id:
                            ecs_list.append(ecs)
                    add_print_ecs(ecs_list)

                    print_data()

