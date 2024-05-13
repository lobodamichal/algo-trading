import boto3 as bt

def create_financial_data_table():
    dynamodb = bt.resource('dynamodb',
                           aws_access_key_id='dummy',
                           aws_secret_access_key='dummy',
                           region_name='local',
                           endpoint_url='http://localhost:8000')

    table_creation_response = dynamodb.create_table(
        TableName='financial_data',
        KeySchema=[
            {
                'AttributeName': 'ticker',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'date',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ticker',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

create_financial_data_table()