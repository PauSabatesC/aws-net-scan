#! /usr/bin/env python3
"""
Get useful AWS data regarding VPC networking in a structured output.
A map af all your subnets, ec2s, route tables and vpcs in your teminal .
"""
__author__ = 'github.com/PauSabatesC'
#__version__ = '1.0'

import argparse
import subprocess
import os
from subprocess import check_output
from pathlib import Path
from .aws_services_data import AwsServicesData
from .analyzer import Analyzer
from .entities import AwsCredentials
from .logger import Logger
from .services import AwsService


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
        prog='aws_net_scan',
        description=__doc__,
        epilog='github.com/PauSabatesC'
    )

    set_cli_args(parser)
    args = parser.parse_args()

    credentials: AwsCredentials = check_aws_credentials(args.profile, log)
    services_data = AwsServicesData(aws_region=credentials.region, log=log)
    aws_service = AwsService(
        aws_secret_key=credentials.aws_secret_key,
        aws_key=credentials.aws_key,
        region=services_data.region,
        log=log
    )
    vpc_analyzer = Analyzer(
        services_data=services_data,
        log=log,
        aws_service=aws_service
    )

    if args.vpc_id:
        vpc_analyzer.search_vpcs(vpc_id=args.vpc_id[0])
    else:
        vpc_analyzer.search_vpcs()
    vpc_analyzer.scan_services()
    services_data.print()
    print('\n')
    log.success('Scan finished successfully.')


def check_aws_credentials(profile: str, log:Logger) -> AwsCredentials:
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
            log.error_and_exit('Windows is not supported yet.')

        if not aws_cred_file.exists():
            log.error_and_exit("AWS credentials file was not found. Please run 'aws configure' to create it.")

    except subprocess.CalledProcessError as e:
        log.error_and_exit("Error finding aws credentials file. ", e)

    try:
        cred_obj = AwsCredentials(
            profile=profile[0],
            aws_key=None,
            aws_secret_key=None,
            region=None
        )
        with open(aws_cred_file) as cred_file:
            for line in cred_file:
                if str(line).split('\n')[0] == '[{}]'.format(profile[0]):
                    aws_key = str(cred_file.readline()).split('\n')[0]
                    aws_secret_key = str(cred_file.readline()).split('\n')[0]
                    cred_obj.aws_key = aws_key.split(' = ')[1]
                    cred_obj.aws_secret_key = aws_secret_key.split(' = ')[1]
                    break

        with open(aws_config_file) as conf_file:
            for line in conf_file:
                if str(line).split('\n')[0] == '[{}]'.format(profile[0]) or \
                        str(line).split('\n')[0] == '[profile {}]'.format(profile[0]):
                    region = str(conf_file.readline()).split('\n')[0]
                    cred_obj.region = region.split(' = ')[1]
                    break
    except OSError as e:
        log.error_and_exit("Error while opening aws credentials or config file. ", e)
    finally:
        if not cred_obj.aws_key or not cred_obj.aws_secret_key or not cred_obj.region:
            log.error_and_exit("AWS credentials are not set up.")
        log.success("AWS credentials obtained successfully from profile {}".format(profile[0]))
        return cred_obj


def main():
    log = Logger(debug_flag=True)
    run(log)


if __name__ == "__main__":
    main()
