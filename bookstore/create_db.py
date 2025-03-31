import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Change region if needed

# Create the table
table = dynamodb.create_table(
    TableName='Book',
    KeySchema=[
        {'AttributeName': 'book_id', 'KeyType': 'HASH'}  # Primary Key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'book_id', 'AttributeType': 'S'}  # String Type
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}  # Capacity settings
)

print("Creating table...")
table.wait_until_exists()
print("Table 'Books' created successfully!")
#test1
