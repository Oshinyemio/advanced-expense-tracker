import json
import boto3
from datetime import datetime
from decimal import Decimal
import uuid

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table = dynamodb.Table('Expenses')
bucket_name = 'expense-tracker-data-ope'

def lambda_handler(event, context):
    print("Received event:", event)

    try:
        body = json.loads(event.get('body', '{}'))

        user_id = body.get('userId')
        amount = body.get('amount')
        category = body.get('category')

        if not user_id or amount is None or not category:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing required fields: userId, amount, or category'})
            }

        amount = Decimal(str(amount))
        description = body.get('description', '')
        timestamp = datetime.utcnow().isoformat()

        item = {
            'userId': user_id,
            'timestamp': timestamp,
            'amount': amount,
            'category': category,
            'description': description
        }

        # Save to DynamoDB
        table.put_item(Item=item)

        # Save to S3 as JSON
        file_name = f"{user_id}/{uuid.uuid4()}.json"
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(item, default=str),
            ContentType='application/json'
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Expense added successfully'})
        }

    except Exception as e:
        print("Error occurred:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
