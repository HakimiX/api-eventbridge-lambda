
# api-eventbridge-lambda

**AWS Services**: <br>
API Gateway, Lambda, EventBridge, KinesisFirehose, S3

* [Architecture](#architecture)
* [Deploy](#deploy)
* [Testing the app](#testing-the-app)
* [Sources](#sources)

## Architecture 

Creates an API Gateway with a POST Method, a Lambda as a data Producer, EventBridge that can
route to different AWS services based on the Rule, two Lambda functions for consumption of data
based on different Rules, and a Kinsesis Firehose that takes data from EventBrdige based on Rule 
to store data in to S3 bucket every 60 seconds.<br>

Requests to the API are sent to EventBridge using the producer Lambda, which triggers the Consumer 
Lambda functions and Kinesis Firehose based on the Rule. 

![](/resources/architecture.png)

### Deploy
Create a virtualenv on MacOS and Linux:
```shell
python3 -m venv .venv
```
After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.
```shell
source .venv/bin/activate
```
Once the virtualenv is activated, you can install the required dependencies.
```
pip install -r requirements.txt
```
Deploy using CDK CLI
```shell
 cdk ls          # list all stacks in the app
 cdk synth       # emits the synthesized CloudFormation template
 cdk deploy      # deploy this stack to your default AWS account/region
 cdk diff        # compare deployed stack with current state
 cdk destroy     # delete all AWS resources
 cdk docs        # open CDK documentation
```

### Testing the App

Upon successful deployment, you should see an API Gateway REST API in the AWS Account. It can be 
tested from the console or the AWS CLI

#### CLI
```shell
# Command
aws apigateway test-invoke-method --rest-api-id <rest-api-id> --resource-id <resource-id> --http-method POST --body <body>

# Example
aws apigateway test-invoke-method --rest-api-id am5fxe1smj --resource-id ikc0hk --http-method POST --body "{\"country\": \"denmark\"}"
```

#### Console
TODO...

### Sources

* [api-eventbridge-lambda](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/api-eventbridge-lambda)
