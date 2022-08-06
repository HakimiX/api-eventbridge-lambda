from cmath import log
import json 
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

""" 
Received EventBridge event: 
{
    "Time": "2019-12-04",
    "Source": "com.mycompany.myapp",
    "Detail": "something...",
    "DetailType": "service_status"
}
"""

def lambda_handler(event, context):
  logger.info(event)

  return {
    'statusCode': 200,
    'body': json.dumps({
      'result': 'testing...'
    }),
  }