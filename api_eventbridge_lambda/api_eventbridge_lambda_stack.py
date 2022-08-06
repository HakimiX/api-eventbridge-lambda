from aws_cdk import (
    aws_lambda,
    aws_iam as iam,
    Stack,
)
from constructs import Construct


class ApiEventbridgeLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        Producer Lambda function with IAM policy (event_policy) attached so it can send events to EventBridge.
        The Lambda function is triggered by the API Gateway. 
        """
        event_producer_lambda = aws_lambda.Function(self, 'eventProducerLambda',
                                                    runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                    handler="event_producer_lambda.lambda_handler",
                                                    code=aws_lambda.Code.from_asset('lambda'))

        # IAM Policy so Lambda can send events to EventBridge
        event_policy = iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                           resources=['*'],
                                           actions=['events:PutEvents'])

        # Attach policy to event_producer_lambda
        event_producer_lambda.add_to_role_policy(event_policy)
        
        """
        Consumer Lambda function #1 with event rule so it can receive events from EventBridge. 
        """