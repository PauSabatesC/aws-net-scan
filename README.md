<h1 align="center">
  aws-net-scan
</h1>

<p align="center">
  <img src="https://github.com/PauSabatesC/aws-net-scan/blob/main/example_cli.png" alt="SockNet logo"/>
</p>

<h3 align="center">
	Get useful AWS data regarding subnets, ec2s, route tables and vpcs in a structured output in your teminal.
</h3>
	

## Installation:
```sh
pip install aws-net-scan
```

## How to use:

The cli will use the AWS profiles you configured wit aws cli that you have already defined in '~/.aws/' and by default it'll use the 'default' aws [profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html), if you want a concrete profile or just info about a concrete vpc run the following commands:

```sh
aws-net-scan --help
```
- Required parameter:

```sh
aws-net-scan --region eu-west-1
```

- Optional parameters:

```sh
aws-net-scan --profile name_profile
```
```sh
aws-net-scan --vpc-id vpc-0ed0X857b02b8b
```


### Project development:

- Setup development environment

```sh
$ mv .env.example dev.env
$ source scripts/setup_env.sh
```
- Cleanup dev environment

```sh
$ source scripts/clean_env.sh
```

- Test:
```sh
$ source scripts/test.sh
```
