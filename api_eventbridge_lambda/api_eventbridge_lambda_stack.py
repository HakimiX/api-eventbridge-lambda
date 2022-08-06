from aws_cdk import (
    aws_lambda,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3 as s3,
    aws_kinesisfirehose as _firehose,
    aws_apigateway as api_gw,
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
        Approved Consumer 1.
        Consumer Lambda function #1 with event rule that targets the consumer Lambda #1
        """
        event_consumer1_lambda = aws_lambda.Function(self, 'eventConsumer1Lambda',
                                                     runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                     handler="event_consumer_lambda.lambda_handler",
                                                     code=aws_lambda.Code.from_asset('lambda'))

        event_consumer1_rule = events.Rule(self, 'eventConsumerLambdaRule',
                                           description="Approved transaction",
                                           event_pattern=events.EventPattern(source=['com.mycompany.myapp']))
        # Event rule target consumer Lambda #1
        event_consumer1_rule.add_target(
            targets.LambdaFunction(handler=event_consumer1_lambda))

        """
        Approved Consumer 2.
        Consumer Lambda function #2 with event rule that targets the consumer Lambda #2
        """
        event_consumer2_lambda = aws_lambda.Function(self, 'eventConsumer2Lambda',
                                                     runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                     handler='event_consumer_lambda.lambda_handler',
                                                     code=aws_lambda.Code.from_asset('lambda'))

        # Event rule
        event_consumer2_rule = events.Rule(self, 'eventConsumer2LambdaRule',
                                           description='Approved Transactions',
                                           event_pattern=events.EventPattern(source=['com.mycompany.myapp']))

        # Event rule target consumer Lambda #2
        event_consumer2_rule.add_target(
            targets.LambdaFunction(handler=event_consumer2_lambda))

        """
        Approved Consumer 3.
        KinesisFirehose received event from EventBridge and stores the data in S3 bucket every 60 seconds.
        """

        # S3 bucket for KinesisFirehose destination
        ingest_bucket = s3.Bucket(self, 'test-ingest-bucket')

        # IAM role for KinesisFirehose
        firehose_role = iam.Role(self, 'kinesisFirehoseRole',
                                 assumed_by=iam.ServicePrincipal('firehose.amazonaws.com'))

        # Create and attach policy the gives permission to write in to the S3 bucket (test-ingest-bucket)
        iam.Policy(
            self, 's3_attr',
            policy_name='s3kinesis',
            statements=[iam.PolicyStatement(
                actions=['s3:*'],
                resources=['arn:aws:s3:::' + ingest_bucket.bucket_name + '/*'])],
            roles=[firehose_role],
        )

        # KinsesisFirehose delivery stream -> S3 bucket
        event_consumer3_kinesisFirehose = _firehose.CfnDeliveryStream(self, 'consumer3firehose',
                                                                      s3_destination_configuration=_firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
                                                                          bucket_arn=ingest_bucket.bucket_arn,
                                                                          buffering_hints=_firehose.CfnDeliveryStream.BufferingHintsProperty(
                                                                              interval_in_seconds=60
                                                                          ),
                                                                          compression_format='UNCOMPRESSED',
                                                                          role_arn=firehose_role.role_arn
                                                                      ))

        # Event Rule
        event_consumer3_rule = events.Rule(self, 'eventConsumer3KinesisRule',
                                           description='Approved transactions',
                                           event_pattern=events.EventPattern(source=['com.mycompany.myapp']))

        # Event Rule target KinesisFirehose
        event_consumer3_rule.add_target(targets.KinesisFirehoseStream(
            stream=event_consumer3_kinesisFirehose))

        """
        API Gateway 
        defines an API Gateway REST API 
        """

        api = api_gw.LambdaRestApi(self, 'sampleAPIEventBridgeMultiConsumer',
        handler=event_producer_lambda,
        proxy=False)

        # API Gateway endpoint and HTTP method
        items = api.root.add_resource('items')
        items.add_method('POST')

