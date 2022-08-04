
# api-eventbridge-lambda

**AWS Services**: <br>
API Gateway, Lambda, EventBridge, KinesisFirehose, S3

* [Architecture](#architecture)
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

### Testing the App

Upon successful deployment, you should see an API Gateway REST API in the AWS Account. It can be 
tested from the console or the AWS CLI

#### CLI
```shell
aws apigateway test-invoke-method --rest-api-id <API ID> --resource-id <RESOURCE ID> --http-method POST --body {"item1":"123","item2":"234"}
```

#### Console
TODO...

### Sources

* [api-eventbridge-lambda](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/api-eventbridge-lambda)


### Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


