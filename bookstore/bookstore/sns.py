import boto3

# Create an SNS client
sns_client = boto3.client("sns", region_name="us-east-1")

# Create an SNS topic
response = sns_client.create_topic(Name="DueDateReminderTopic")
sns_topic_arn = response["TopicArn"]

print(f"SNS Topic ARN: {sns_topic_arn}")
