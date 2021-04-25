from .entities import AwsObjectData
from .logger import LogColors
from tabulate import tabulate


def print_vpc_data(vpc_data: AwsObjectData):
    print('\n' +
          LogColors.START_TITLE + 'VPC: ' + vpc_data.vpc_id + LogColors.INTERSECTION +
          LogColors.WARNING + 'Name: ' + vpc_data.name + LogColors.INTERSECTION +
          LogColors.WARNING + 'CIDR: ' + vpc_data.cidr + LogColors.INTERSECTION +
          LogColors.WARNING + 'InetGateway: ' + vpc_data.igw + LogColors.INTERSECTION

          )


def print_subnet_data(subnet_data: AwsObjectData):
    print(
        LogColors.START_SUBTITLE + LogColors.START_SUBTITLE +
        'SUBNET: ' + subnet_data.id + LogColors.INTERSECTION + LogColors.BLUE1 +
        'Name: ' + subnet_data.name + LogColors.INTERSECTION + LogColors.BLUE1 +
        'CIDR: ' + subnet_data.cidr
    )

    if subnet_data.route_tables:
        str_routes = ''
        for route in subnet_data.route_tables:
            if 'GatewayId' in route and 'DestinationCidrBlock' in route:
                str_routes += route['DestinationCidrBlock'] + '->' + route['GatewayId'] + ' | '
            elif 'NatGatewayId' in route and 'DestinationCidrBlock' in route:
                str_routes += route['DestinationCidrBlock'] + '->' + route['NatGatewayId'] + ' | '

        print(
            LogColors.START_SUBTITLE + LogColors.START_SUBTITLE + LogColors.START_SUBTITLE +
            'ROUTES: ' + str_routes
        )


def print_ec2s(ec2_list):
    data = []
    for ec2 in ec2_list:
        data.append([
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            'EC2: ' + ec2.id,
            'Name: ' + ec2.name,
            ec2.state,
            ec2.instance_type,
            'Private IP: ' + ec2.private_ip,
            'Public IP: ' + ec2.public_ip
        ]
        )

    if data:
        print(tabulate(data, tablefmt="plain"))

