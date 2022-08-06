import logging
import datetime
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
  eventbridge_client = boto3.client('events')
  request_body = event['body']
  if request_body is None:
    request_body = ""
  
  # Structure of EventBridge Event
  eventbridge_event = {
    'Time': datetime.datetime.now(),
    'Source': 'com.mycompany.myapp',
    'Detail': request_body,
    'DetailType': 'service_status'
  }
  logger.info(eventbridge_event)

  # Send event to EventBridge
  response = eventbridge_client.put_events(
    Entries=[
      eventbridge_event
    ]
  )
  logger.info(response)

  # Return success response to API Gateway
  return {
    'statusCode': 200,
    'body': json.dumps({
      'result': 'from producer'
    })
  }
