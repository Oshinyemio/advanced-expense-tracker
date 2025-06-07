import boto3
import csv
import io

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ExpenseTracker')

def lambda_handler(event, context):
    user_id = event['queryStringParameters']['userId']
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(user_id)
    )
    items = response['Items']

    # Convert to CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=items[0].keys())
    writer.writeheader()
    writer.writerows(items)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=expenses_{user_id}.csv'
        },
        'body': output.getvalue()
    }
