import boto3
import csv
import io

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Expenses')

def lambda_handler(event, context):
    if not event.get('queryStringParameters') or not event['queryStringParameters'].get('userId'):
        return {
            'statusCode': 400,
            'body': 'Missing userId parameter'
        }

    user_id = event['queryStringParameters']['userId']

    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(user_id)
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error querying DynamoDB: {e}"
        }

    items = response.get('Items', [])
    if not items:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename=expenses_{user_id}.csv',
                'Access-Control-Allow-Origin': '*'
            },
            'body': ''
        }

    try:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(items[0].keys()))
        writer.writeheader()
        writer.writerows(items)
        csv_string = output.getvalue()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error converting to CSV: {e}"
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=expenses_{user_id}.csv',
            'Access-Control-Allow-Origin': '*'
        },
        'body': csv_string
    }
