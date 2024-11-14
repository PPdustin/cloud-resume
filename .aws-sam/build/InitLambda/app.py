import boto3
import os
import cfnresponse

def lambda_handler(event, context):
    # Get table name from environment variable
    table_name = os.environ['TABLE_NAME']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
            initdata = {'page': 'home_page', 'visits': 0}
            table.put_item(Item=initdata)
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                'Message': 'Data initialized successfully'
            })
            
        elif event['RequestType'] == 'Delete':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                'Message': 'Delete request acknowledged'
            })
        else:
            cfnresponse.send(event, context, cfnresponse.FAILED, {
            'Error': "Else if handling failed"
        })
            
    except Exception as e:
        print(f"Error: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {
            'Error': str(e)
        })