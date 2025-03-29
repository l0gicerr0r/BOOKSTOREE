import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create a table for storing user data
table_name = "Users"
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {'AttributeName': 'username', 'KeyType': 'HASH'}  # Partition Key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'username', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)

# Wait for the table to be created
table.wait_until_exists()
print(f"Table '{table_name}' created successfully!")
