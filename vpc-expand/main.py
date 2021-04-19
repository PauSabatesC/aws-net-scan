#! /usr/bin/env python3
"""
Shows all AWS services inside a VPC .
"""
__author__ = 'github.com/PauSabatesC'
__version__ = '1.0'

import argparse
import subprocess
import os
from subprocess import check_output
from pathlib import Path
from aws_services_data import AwsServicesData
from analyzer import Analyzer
from entities import AwsCredentials
from logger import Logger


def set_cli_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--vpc-id',
        nargs=1,
        help='vpc id  to search from'
    )

    parser.add_argument(
        '--profile',
        nargs=1,
        help='AWS credentials profile located in ~/.aws/credentials',
        default=['default']
    )


def run(log: Logger):
    parser = argparse.ArgumentParser(
        prog='vpc-expand',
        description=__doc__,
        epilog='github.com/PauSabatesC'
    )
    log.error('xd', Exception)
    set_cli_args(parser)
    args = parser.parse_args()

    credentials: AwsCredentials = check_aws_credentials(args.profile)
    services_data = AwsServicesData(aws_region=credentials.region)
    vpc_analyzer = Analyzer(
        aws_access_key=credentials.aws_access_key,
        aws_key=credentials.aws_key,
        services_data=services_data
    )

    if args.vpc_id:
        vpc_analyzer.search_vpcs(vpc_id=args.vpc_id)
    else:
        vpc_analyzer.search_vpcs()

    #services_data.print()


def check_aws_credentials(profile: str) -> AwsCredentials:
    """
    Search into aws folder the credentials of the indicated profile.
    If not profile received the default profile is 'default'.
    """
    try:
        user = check_output(['whoami']).decode("utf-8").split('\n')[0]

        if os.name == 'posix':
            aws_cred_file = Path("/home/{}/.aws/credentials".format(user))
            aws_config_file = Path("/home/{}/.aws/config".format(user))
        if os.name == 'nt':
            print("Windows is not supported yet.")
            exit(1)

        if not aws_cred_file.exists():
            print("AWS credentials file was not found. Please run 'aws configure' to create it.")
            exit(1)
    except subprocess.CalledProcessError as e:
        print("Error finding aws credentials file. " + e)

    try:
        cred_obj = AwsCredentials(
            profile=profile[0],
            aws_key=None,
            aws_access_key=None,
            region=None
        )
        with open(aws_cred_file) as cred_file:
            for line in cred_file:
                if str(line).split('\n')[0] == '[{}]'.format(profile[0]):
                    aws_key = str(cred_file.readline()).split('\n')[0]
                    aws_access_key = str(cred_file.readline()).split('\n')[0]
                    cred_obj.aws_key = aws_key.split(' = ')[1]
                    cred_obj.aws_access_key = aws_access_key.split(' = ')[1]
                    break

        with open(aws_config_file) as conf_file:
            for line in conf_file:
                if str(line).split('\n')[0] == '[{}]'.format(profile[0]) or \
                        str(line).split('\n')[0] == '[profile {}]'.format(profile[0]):
                    region = str(conf_file.readline()).split('\n')[0]
                    cred_obj.region = region.split(' = ')[1]
                    break
    except OSError as e:
        print("Error while opening aws credentials or config file. " + e)
    finally:
        if not cred_obj.aws_key or not cred_obj.aws_access_key or not cred_obj.region:
            print("AWS credentials are not set up.")
            exit(1)
        print("AWS credentials obtained successfully from profile {}".format(profile[0]))
        return cred_obj


if __name__ == "__main__":
    log = Logger(debug_flag=True)
    run(log)
