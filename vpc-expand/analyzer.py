import boto3
from entities import AwsObjectData
from aws_services_data import AwsServicesData
from logger import Logger
import utils


class Analyzer:
    def __init__(self, services_data: AwsServicesData,
                 aws_key: str, aws_secret_key: str, log: Logger):
        self.log = log
        self.data = services_data
        self.aws_session = boto3.Session(
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret_key,
            region_name=services_data.region
        )
        self.aws_ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret_key,
            region_name=services_data.region
        )
        self.aws_ec2_res = self.aws_session.resource('ec2')

    def search_vpcs(self, vpc_id=None):
        if vpc_id:
            response = self.aws_ec2_client.describe_vpcs(VpcIds=[vpc_id])
            res_ok = utils.validate_aws_response(response)
            if res_ok:

                self.data.add_vpc(AwsObjectData(
                    vpc_id=vpc_id,
                    self_id=vpc_id,
                    name='xd'
                )
                )
        else:
            print(utils.pretty_json(self.aws_ec2_client.describe_vpcs()))
            pass

# VPC_IDS=$(aws ec2 describe-vpcs --region eu-west-2 --filters 'Name=tag:Name,Values=pmUtilts-VPC-VPN' | grep VpcId | awk '{ print $2 }' | sed 's/[\",]//g')
