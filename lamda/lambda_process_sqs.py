import boto3
import json

# Connect to AWS
sqs_client = boto3.client('sqs', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')

# SQS Queue URL and SNS Topic ARN (Replace with actual values)
queue_url = "https://sqs.us-east-1.amazonaws.com/264987204337/DueDateReminderQueue"  # Replace this!
sns_topic_arn = "arn:aws:sns:us-east-1:264987204337:DueDateReminderTopic"  # Replace this!

def process_sqs_messages(event, context):
    response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)

    if "Messages" in response:
        for message in response["Messages"]:
            body = json.loads(message["Body"])
            user_email = body["email"]
            book_name = body["book_name"]
            due_date = body["due_date"]

            sns_message = f"Reminder: Your book '{book_name}' is due on {due_date}. Please return it on time!"

            # Publish message to SNS
            sns_client.publish(TopicArn=sns_topic_arn, Message=sns_message, Subject="Book Due Reminder")

            print(f"Reminder sent to {user_email} for book '{book_name}'")

            # Delete the processed message
            sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])

    return {"statusCode": 200, "body": "Reminders Sent"}
