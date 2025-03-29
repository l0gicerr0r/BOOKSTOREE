import boto3

# Initialize the SQS client
sqs = boto3.client("sqs", region_name="us-east-1")  # Change the region if needed

# Queue name
queue_name = "BookBorrowQueue"

def create_sqs_queue():
    try:
        response = sqs.create_queue(
            QueueName=queue_name,
            Attributes={
                "VisibilityTimeout": "30",  # Message visibility timeout (in seconds)
                "MessageRetentionPeriod": "86400"  # Retain messages for 1 day (in seconds)
            }
        )
        queue_url = response["QueueUrl"]
        print(f"Queue '{queue_name}' created successfully!")
        print(f"Queue URL: {queue_url}")
        return queue_url
    except Exception as e:
        print(f"Error creating queue: {e}")

# Call the function
if __name__ == "__main__":
    create_sqs_queue()
