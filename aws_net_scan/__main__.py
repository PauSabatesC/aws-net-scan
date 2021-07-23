#! /usr/bin/env python3
"""
Get useful AWS data regarding VPC networking in a structured output.
A map af all your subnets, ec2s, route tables and vpcs in your teminal .
"""
__author__ = 'github.com/PauSabatesC'
__version__ = '0.5.0'

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
        required=True
    )


def run(log: Logger):
    parser = argparse.ArgumentParser(
        prog='aws_net_scan',
        description=__doc__,
        epilog='Version: ' + __version__ + ' Developer: github.com/PauSabatesC'
    )

    set_cli_args(parser)
    args = parser.parse_args()

    services_data = AwsServicesData(log=log)

    aws_service = AwsService(
        profile_name=args.profile[0],
        log=log
    )
    vpc_analyzer = Analyzer(
        services_data=services_data,
        log=log,
        aws_service=aws_service
    )
    
    log.success('Scanning data...')
    if args.vpc_id:
        vpc_analyzer.search_vpcs(vpc_id=args.vpc_id[0])
    else:
        vpc_analyzer.search_vpcs()
    vpc_analyzer.scan_services()
    services_data.print()
    print('\n')
    log.success('Scan finished successfully.')


def main():
    log = Logger(debug_flag=True)
    run(log)


if __name__ == "__main__":
    main()
