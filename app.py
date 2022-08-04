#!/usr/bin/env python3
import os

import aws_cdk as cdk

from api_eventbridge_lambda.api_eventbridge_lambda_stack import ApiEventbridgeLambdaStack


app = cdk.App()
ApiEventbridgeLambdaStack(app, "ApiEventbridgeLambdaStack")

app.synth()
