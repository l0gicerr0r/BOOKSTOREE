import boto3
import zipfile
import io
import json

# AWS configuration
AWS_REGION = "us-east-1"
LAMBDA_ROLE_ARN = "arn:aws:iam::264987204337:role/LabRole"  # Replace with your IAM Role ARN
SQS_QUEUE_ARN = "arn:aws:sqs:us-east-1:264987204337:DueDateReminderQueue"  # Replace with actual queue ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:264987204337:DueDateReminderTopic"  # Replace with actual topic ARN

# List of Lambda functions to deploy
FUNCTIONS = [
    {
        "FunctionName": "DueDateReminderLambda",
        "Handler": "lambda_due_reminder.send_due_reminders",  # FileName.functionName
        "Description": "Sends reminders for books due in 5 days and sends them to SQS"
    },
    {
        "FunctionName": "ProcessDueDateReminderLambda",
        "Handler": "lambda_process_sqs.process_sqs_messages",  # FileName.functionName
        "Description": "Processes SQS messages and sends SNS reminders for due books"
    }
]

# Initialize AWS clients
lambda_client = boto3.client("lambda", region_name=AWS_REGION)
event_source_client = boto3.client("lambda", region_name=AWS_REGION)

def package_single_zip():
    """
    Zips all .py files in the lamda/ folder into a single in-memory ZIP.
    Returns the bytes of that ZIP.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add Lambda function files from the 'lamda' folder
        zf.write("lamda/lambda_due_reminder.py", "lambda_due_reminder.py")
        zf.write("lamda/lambda_process_sqs.py", "lambda_process_sqs.py")

    zip_buffer.seek(0)
    return zip_buffer.read()

def create_or_update_lambda(function_name, handler, description, zip_content):
    """
    Creates or updates a Lambda function with the given parameters.
    """
    try:
        lambda_client.get_function(FunctionName=function_name)
        print(f"Updating Lambda function: {function_name}")

        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content,
            Publish=True
        )

        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Role=LAMBDA_ROLE_ARN,
            Handler=handler,
            Runtime="python3.9",
            Description=description,
            Timeout=60,
            MemorySize=128
        )

        print(f"Lambda function {function_name} updated successfully!")

    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"Creating new Lambda function: {function_name}")

        lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.9",
            Role=LAMBDA_ROLE_ARN,
            Handler=handler,
            Code={"ZipFile": zip_content},
            Description=description,
            Publish=True,
            Timeout=60,
            MemorySize=128
        )

        print(f"Lambda function {function_name} created successfully!")

def add_sqs_trigger():
    """Adds an SQS trigger to DueDateReminderLambda."""
    try:
        response = event_source_client.create_event_source_mapping(
            EventSourceArn=SQS_QUEUE_ARN,
            FunctionName="DueDateReminderLambda",
            BatchSize=10,
            Enabled=True
        )
        print(f"SQS trigger added to DueDateReminderLambda: {response}")
    except Exception as e:
        print(f"Error adding SQS trigger: {str(e)}")


def add_sns_trigger():
    """Adds an SNS trigger to ProcessDueDateReminderLambda."""
    try:
        response = lambda_client.add_permission(
            FunctionName="ProcessDueDateReminderLambda",
            StatementId="SNSInvokePermission",
            Action="lambda:InvokeFunction",
            Principal="sns.amazonaws.com",
            SourceArn=SNS_TOPIC_ARN
        )
        print(f"SNS trigger added to ProcessDueDateReminderLambda: {response}")
    except Exception as e:
        print(f"Error adding SNS trigger: {e}")

def main():
    zip_content = package_single_zip()
    for func in FUNCTIONS:
        create_or_update_lambda(
            function_name=func["FunctionName"],
            handler=func["Handler"],
            description=func["Description"],
            zip_content=zip_content
        )
    add_sqs_trigger()
    add_sns_trigger()
    print("\nAll Lambda functions deployed with triggers successfully!")

if __name__ == "__main__":
    main()