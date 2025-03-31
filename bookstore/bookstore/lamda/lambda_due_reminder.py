import boto3
import datetime
import json

# Connect to AWS
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')

# Table and SQS Queue URL (Replace with actual values)
table = dynamodb.Table("Borrow")
queue_url = "https://sqs.us-east-1.amazonaws.com/264987204337/DueDateReminderQueue"
  # Replace this!

def send_due_reminders(event, context):
    today = datetime.date.today()
    five_days_later = today + datetime.timedelta(days=5)

    # Scan the Borrow table
    response = table.scan()
    items = response.get("Items", [])

    for item in items:
        due_date_str = item.get("due_date")
        user_email = item.get("email")
        book_name = item.get("book_name")

        if due_date_str:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            
            if due_date == five_days_later:
                message_body = json.dumps({
                    "email": user_email,
                    "book_name": book_name,
                    "due_date": due_date_str
                })
                
                # Send message to SQS
                sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
                print(f"Added to SQS: {user_email} for book '{book_name}'")

    return {"statusCode": 200, "body": "Users added to SQS"}
