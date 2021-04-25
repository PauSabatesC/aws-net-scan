# aws-net-scan

Get useful AWS data regarding VPC networking in a structured output.
A map af all your subnets, ec2s, route tables and vpcs in your teminal .

(project under early development)

- Setup development environment

```sh
$ mv .env.example dev.env
$ source scripts/setup_env.sh dev
```
- Cleanup dev environment

```sh
$ source scripts/clean_env.sh dev
```

- TODOs:

	- get rds in vpcs
	- get ecs in vpcs
	- add loading animation
	- option to filter services with tags
	- add tests
	- add gh actions, tux.ini, setup.py 
	- -vvv option to show more aws data
