from .entities import AwsObjectData
from .logger import LogColors
from tabulate import tabulate

data = []


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


def add_print_ec2s(ec2_list):
    for ec2 in ec2_list:
        value = [
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            'EC2: ' + ec2.id,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Name: ' + ec2.name,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Status: ' + ec2.state,
            LogColors.INTERSECTION + LogColors.BLUE2 + ec2.instance_type,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Private IP: ' + ec2.private_ip,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Public IP: ' + ec2.public_ip
        ]
        data.append({'type': 'ec2', 'value': value})


def add_print_rds(rds_list):
    for rds in rds_list:
        value = [
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            'RDS: ' + rds.id,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Engine: ' + rds.engine,
        ]
        data.append({'type': 'rds', 'value': value})


def add_print_elb(elb_list):
    for elb in elb_list:
        value = [
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            'ELB: ' + elb.id,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Type: ' + elb.type,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Status: ' + elb.state,
        ]
        data.append({'type': 'elb', 'value': value})


def add_print_ecs(ecs_list):
    for ecs in ecs_list:
        value = [
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            LogColors.START_SUBTITLE_2 + LogColors.START_SUBTITLE_2 +
            'ECS: ' + ecs.id,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Service: ' + ecs.service,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Status: ' + ecs.status,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Cluster: ' + ecs.cluster,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Private IP: ' + ecs.private_ip,
            LogColors.INTERSECTION + LogColors.BLUE2 + 'Public IP: ' + ecs.public_ip,
        ]
        data.append({'type': 'ecs', 'value': value})


def print_data():
    if data:
        data_sorted = sorted(data, key=lambda i: (i['type']))
        data_final = []
        for element in data_sorted:
            data_final.append(element['value'])
        print(tabulate(data_final, tablefmt="plain"))
    data.clear()
