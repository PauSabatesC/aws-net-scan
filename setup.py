from setuptools import setup, find_packages

with open("README.md", "rb") as f:
    readme = f.read().decode("utf-8")

setup(
    name='aws-net-scan',
    version='0.1.0',
    description='Get useful AWS data regarding VPC networking in a structured output.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='github.com/PauSabatesC',
    url='https://github.com/PauSabatesC/aws-net-scan',
    license='Apache 2.0',
    python_requires=">=3.6, <4",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(include=['aws_net_scan']),
    install_requires=[
        'boto3==1.17.53',
        'botocore==1.20.53',
        'tabulate==0.8.9',
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    extras_require={
        'deploy': ['twine'],
    },
    entry_points={'console_scripts': ['aws-net-scan= aws_net_scan.__main__:main']},
    keywords=['aws', 'network', 'scan', 'aws-net-scan', 'cloud', 'vpc', 'ec2'],
)
