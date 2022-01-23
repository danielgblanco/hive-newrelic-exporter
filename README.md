# Hive New Relic Exporter
AWS Lambda deployment to export metrics from Hive Home to New Relic.

## Requirements
To install the Hive New Relic Exporter you need:

* `serverless`: in order to deploy the AWS Lambda function ([more info](https://www.serverless.com/framework/docs/getting-started))
* `docker`: needed to package dependencies with `serverless-python-requirements` if you don't run this on Linux

After `serverless` is installed, run:

```bash
serverless plugin install --name serverless-python-requirements
```

## Deploying
The deployment details are contained in `serverless.yml`, including the AWS region to deploy to.

The function uses environment variables for credentials. The recommended way is to use SSM Parameter Store
  `SecureString` parameters. You can add your variables as explained in the [original docs](https://www.serverless.com/framework/docs/providers/aws/guide/variables#reference-variables-using-the-ssm-parameter-store)

You can use `NEWRELIC_REGION` (US or EU) and `NEWRELIC_INSERT_KEY` (an Insights Insert key) from New Relic.

In order to get `ID_TOKEN`, `REFRESH_TOKEN` and `ACCESS_TOKEN` to communicate with the Hive API, run:

```bash
make login
```

After entering username and password and passing 2FA, you'll get the values to add to SSM.

Once all values are in SSM and the paths set in `serverless.yml`, in order to deploy, run:

```bash
make deploy
```

For more information about deploying see the [official Serverless docs](https://www.serverless.com/framework/docs/providers/aws/guide/deploying).

