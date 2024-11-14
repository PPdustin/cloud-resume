import json
import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    
    try:
        response = table.get_item(Key={'page': "home_page"})
        
        if 'Item' in response:
            current_count = response['Item']['visits']
        else:
            current_count = 0
        
        new_count = current_count + 1
        
        table.update_item(
            Key={'page': "home_page"},
            UpdateExpression="SET visits = :val",
            ExpressionAttributeValues={':val': new_count}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': f'Visitor count updated to {new_count}',
                'visitor_count': int(new_count)
            })
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating visitor count',
                'error': str(e)
            })
        }
 