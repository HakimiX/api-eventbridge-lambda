from aws_cdk import (
    aws_lambda,
    Stack,
)
from constructs import Construct


class ApiEventbridgeLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Producer Lambda
        event_producer_lambda = aws_lambda.Function(self, 'eventProducerLambda',
                                                    runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                    handler="event_producer_lambda.lambda_handler",
                                                    code=aws_lambda.Code.from_asset('lambda'))
