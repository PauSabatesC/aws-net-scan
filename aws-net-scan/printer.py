from entities import AwsObjectData
from logger import LogColors


def print_vpc_data(vpc_data: AwsObjectData):
    print('\n' +
          LogColors.START_TITLE + 'VPC: ' + vpc_data.vpc_id + LogColors.INTERSECTION +
          LogColors.BLUE2 + 'Name: ' + vpc_data.name + LogColors.INTERSECTION +
          LogColors.BLUE2 + 'CIDR: ' + vpc_data.cidr + LogColors.INTERSECTION +
          LogColors.BLUE2 + 'InetGateway: ' + vpc_data.igw + LogColors.INTERSECTION

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
            if 'GatewayId' in route:
                str_routes += route['DestinationCidrBlock'] + '->' + route['GatewayId'] + ' | '
            elif 'NatGatewayId' in route:
                str_routes += route['DestinationCidrBlock'] + '->' + route['NatGatewayId'] + ' | '

        print(
            LogColors.START_SUBTITLE + LogColors.START_SUBTITLE + LogColors.START_SUBTITLE +
            'ROUTES: ' + str_routes
        )


def print_ec2s(ec2:AwsObjectData):
    print(
        LogColors.START_SUBTITLE + LogColors.START_SUBTITLE +
        LogColors.START_SUBTITLE + LogColors.START_SUBTITLE +
        'EC2: ' + ec2.id + LogColors.INTERSECTION + LogColors.BLUE1 +
        'Name: ' + ec2.name + LogColors.INTERSECTION + LogColors.BLUE1 +
         ec2.state + LogColors.INTERSECTION + LogColors.BLUE1 +
        ec2.instance_type + LogColors.INTERSECTION + LogColors.BLUE1 +
        'Private IP: ' + ec2.private_ip + LogColors.INTERSECTION + LogColors.BLUE1 +
        'Public IP: ' + ec2.public_ip + LogColors.INTERSECTION + LogColors.BLUE1
    )