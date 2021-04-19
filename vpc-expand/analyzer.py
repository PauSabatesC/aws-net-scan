import boto3
from entities import AwsObjectData
from aws_services_data import AwsServicesData


class Analyzer:
    def __init__(self, services_data: AwsServicesData,
                 aws_key: str, aws_access_key: str):
        self.aws_session = boto3.Session(
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_access_key
        )
        self.aws_ec2 = self.aws_session.resource('ec2')
        self.data = services_data

    def search_vpcs(self, vpc_id=None):
        if vpc_id:
            # get data of vpc
            self.data.add_vpc(AwsObjectData(
                vpc_id=vpc_id,
                self_id=vpc_id,
                name='xd'
            )
            )
        else:
            # search all vpcs in region and its data
            self.data.ecs
            pass

# VPC_IDS=$(aws ec2 describe-vpcs --region eu-west-2 --filters 'Name=tag:Name,Values=pmUtilts-VPC-VPN' | grep VpcId | awk '{ print $2 }' | sed 's/[\",]//g')
