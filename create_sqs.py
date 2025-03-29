import boto3

# Connect to SQS
sqs_client = boto3.client('sqs', region_name='us-east-1')

# Create an SQS queue
response = sqs_client.create_queue(QueueName="DueDateReminderQueue")
queue_url = response["QueueUrl"]

print(f"SQS Queue Created: {queue_url}")
