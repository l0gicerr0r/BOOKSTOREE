import boto3

# Initialize the DynamoDB resource (adjust region as needed)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

TABLE_NAME = "Borrow"

# Function to check and delete the table if it exists
def delete_table_if_exists(table_name):
    try:
        table = dynamodb.Table(table_name)
        table.load()  # Check if the table exists
        print(f"Table '{table_name}' exists. Deleting...")
        table.delete()
        table.wait_until_not_exists()  # Wait for deletion to complete
        print(f"Table '{table_name}' deleted successfully.")
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        print(f"Table '{table_name}' does not exist. Proceeding with creation.")

# Delete the table if it exists
delete_table_if_exists(TABLE_NAME)

# Creating the Borrow table
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    KeySchema=[
        {'AttributeName': 'username', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'book_id', 'KeyType': 'RANGE'}   # Sort key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'username', 'AttributeType': 'S'},  # Primary key
        {'AttributeName': 'book_id', 'AttributeType': 'S'},    # Sort key
        {'AttributeName': 'borrow_date', 'AttributeType': 'S'},  # GSI key
        {'AttributeName': 'due_date', 'AttributeType': 'S'},     # GSI key
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'BorrowDateIndex',
            'KeySchema': [{'AttributeName': 'borrow_date', 'KeyType': 'HASH'}],  # GSI partition key
            'Projection': {'ProjectionType': 'ALL'},  # Include all attributes
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        },
        {
            'IndexName': 'DueDateIndex',
            'KeySchema': [{'AttributeName': 'due_date', 'KeyType': 'HASH'}],  # GSI partition key
            'Projection': {'ProjectionType': 'ALL'},  # Include all attributes
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        }
    ]
)

print("Creating table...")

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
print(f"Table '{TABLE_NAME}' created successfully. Table status:", table.table_status)




