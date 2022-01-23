from setuptools import setup, find_packages

setup(
    name='hive-newrelic-exporter',
    version='0.1.0',
    packages=find_packages(include=['hive_newrelic_exporter', 'hive_newrelic_exporter.*']),
    install_requires=[
        'pyhiveapi>=0.4.3',
        'newrelic-telemetry-sdk>=0.4.2'
    ]
)
