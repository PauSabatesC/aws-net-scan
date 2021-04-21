from entities import AwsObjectData
from logger import LogColors


def print_vpc_data(vpc_data: AwsObjectData):
    print(
          LogColors.START_TITLE + 'VPC: ' + vpc_data.vpc_id + LogColors.INTERSECTION +
          LogColors.BLUE2 + 'CIDR: ' + vpc_data.cidr + LogColors.INTERSECTION +
          LogColors.BLUE2 + 'InetGateway: ' + vpc_data.igw
          #LogColors.OKCYAN + 'TAGS: ' + str(vpc_data.tags)
          )


def print_subnet_data(subnet_data: AwsObjectData):
    print(
        LogColors.START_SUBTITLE + LogColors.START_SUBTITLE +
        'SUBNET: ' + subnet_data.id + LogColors.INTERSECTION + LogColors.BLUE1 +
        'CIDR: ' + subnet_data.cidr
        #LogColors.OKCYAN + 'TAGS: ' + str(subnet_data.tags)
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
