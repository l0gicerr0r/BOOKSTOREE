import boto3
import json

from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings
from django.contrib import messages  # Import Django messages
from boto3.dynamodb.conditions import Key
from datetime import datetime
from bookreturncalculatorPkg.bookreturncalculator import BookReturnCalculator

# from bookreturncalculator import BookReturnCalculator


# calculator = BookReturnCalculator(borrow_period_days=30)

SQS_QUEUE_URL = settings.SQS_QUEUE_URL
DYNAMODB_USERS_TABLE = settings.DYNAMODB_USERS_TABLE
DYNAMODB_BOOKS_TABLE = settings.DYNAMODB_BOOKS_TABLE
DYNAMODB_BORROW_TABLE = settings.DYNAMODB_BORROW_TABLE

# Initialize AWS clients/resources
sqs = boto3.client("sqs", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
users_table = dynamodb.Table(DYNAMODB_USERS_TABLE)
books_table = dynamodb.Table(DYNAMODB_BOOKS_TABLE)
borrow_table = dynamodb.Table(DYNAMODB_BORROW_TABLE)


# def send_borrow_request_to_queue(username: str, book_id: str) -> dict:
#     """
#     Sends a borrow request message to the SQS queue.
    
#     Args:
#         username (str): The username of the borrower.
#         book_id (str): The book_id of the book to borrow.
    
#     Returns:
#         dict: The response from the SQS send_message API.
#     """
#     message = {
#         "username": username,
#         "book_id": book_id,
#         "request_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
#     }
    
#     response = sqs.send_message(
#         QueueUrl=SQS_QUEUE_URL,
#         MessageBody=json.dumps(message)
#     )
#     return response

def send_borrow_request_to_queue(username, book_id,due_date):
    """
    Send the borrow request to SQS for further processing.
    """
    try:
        message_body = {
            'username': username,
            'book_id': book_id,
            'borrow_date': datetime.today().strftime('%Y-%m-%d')
        }

        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=str(message_body)
        )

        print("SQS Message Sent:", response)
        return response

    except Exception as e:
        print("Error sending message to SQS:", str(e))
        return None



# def process_borrow_requests_from_queue(request) -> None:
#     """
#     Processes borrow request messages from the SQS queue. For each message:
#       - Retrieves user and book details from DynamoDB.
#       - Checks if the book is available.
#       - Inserts a borrow record into the Borrow table.
#       - Updates the user's borrowed_books list in the Users table.
#       - Decrements the book quantity in the Book table.
#       - Deletes the message from the queue.
#       - Checks if there are overdue books and calculates fine.
#     """
#     try:
#         # Retrieve up to 5 messages from SQS (adjust as needed)
#         response = sqs.receive_message(
#             QueueUrl=SQS_QUEUE_URL,
#             MaxNumberOfMessages=5,
#             WaitTimeSeconds=10
#         )
#         messages_list = response.get("Messages", [])
        
#         if not messages_list:
#             print("No new borrow requests in the queue.")
#             return
#         for message in messages_list:
#             body = json.loads(message["Body"])
#             username = body["username"]
#             book_id = body["book_id"]
#             request_time = body["request_time"]
#             print(book_id)

#             print(f"Processing borrow request: {username} wants to borrow book with ID '{book_id}' at {request_time}")

#             # Fetch user data from Users table
#             user_response = users_table.get_item(Key={"username": username})
#             user_data = user_response.get("Item", {})
            
#             if not user_data:
#                 print(f"User {username} not found in the database. Skipping message.")
#                 # Send response to user using Django messages
#                 messages.error(request, f"User not found.")
#                 continue
            
#             # Query Borrow table for all books borrowed by this user
#             borrowed_response = borrow_table.query(
#                 KeyConditionExpression=Key('username').eq(username)
#             )
#             borrowed_books = borrowed_response.get('Items', [])
#             print("borrowed_books", borrowed_books)
            
#             # Check if user has reached maximum borrow limit (5 books)
#             if len(borrowed_books) >= 5:                                                              
#                 print(f"User {username} has reached the maximum borrow limit of 5 books. Skipping message.")
#                 # Send response to user using Django messages
#                 messages.error(request, f"You have reached the maximum borrow limit of 5 books.")
#                 continue
            
#             # Check if user already has this book borrowed
#             if any(book["book_id"] == book_id for book in borrowed_books):
#                 print(f"User {username} already has this book borrowed. Skipping message.")
#                 # Send response to user using Django messages
#                 messages.error(request, f"You already have this book borrowed.")
#                 continue

#             # Fetch book data from Book table
#             book_response = books_table.get_item(Key={"book_id": book_id})
#             book_data = book_response.get("Item", {})
#             if not book_data:
#                 print(f"Book with ID '{book_id}' not found in the database. Skipping message.")
#                 # Send response to user using Django messages
#                 messages.error(request, f"Book not found.")
#                 continue

#             # Check if the book is available
#             current_quantity = book_data.get("quantity", "0")  # Default to "0" if quantity is not present
#             try:
#                 current_quantity = int(current_quantity)
#             except ValueError:
#                 print(f"Invalid quantity value for book ID '{book_id}': {current_quantity}. Treating as 0.")
#                 current_quantity = 0

#             if current_quantity <= 0:
#                 print(f"Book with ID '{book_id}' is out of stock. Skipping message.")
#                 # Send response to user using Django messages
#                 messages.error(request, f"This book is currently out of stock.")
#                 continue
#             print(current_quantity)

#             # Create a borrow record
#             borrow_date = request_time
#             due_date = (datetime.strptime(request_time.split()[0], "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
#             borrow_record = {
#                 "username": username,
#                 "book_id": book_id,
#                 "borrow_date": borrow_date,
#                 "due_date": due_date
#             }
#             borrow_table.put_item(Item=borrow_record)

#             # Decrement the quantity of the book
#             books_table.update_item(
#                 Key={"book_id": book_id},
#                 UpdateExpression="SET quantity = :new_quantity",
#                 ExpressionAttributeValues={
#                     ":new_quantity": str(current_quantity - 1)  # Convert to string for DynamoDB
#                 }
#             )

#             # Delete the processed message from SQS
#             sqs.delete_message(
#                 QueueUrl=SQS_QUEUE_URL,
#                 ReceiptHandle=message["ReceiptHandle"]
#             )

#             # Send success response to user using Django messages
#             messages.success(request, f"You have successfully borrowed the book. Due date: {due_date}")

#             print(f"Borrow request for book ID '{book_id}' by {username} processed successfully.")

#     except (NoCredentialsError, PartialCredentialsError) as e:
#         print("AWS Credentials Error:", str(e))
#     except Exception as e:
#         print("Error processing borrow requests:", str(e))
#         # If you want to capture this error in messages, you can do:
#         # messages.error(request, f"An error occurred: {str(e)}")

# 
# 


from bookreturncalculatorPkg.bookreturncalculator import BookReturnCalculator

def process_borrow_requests_from_queue():
    """
    Fetch messages from the SQS queue and process borrow requests.
    This function should be run as a background task.
    """
    try:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,  # Fetch up to 10 messages at a time
            WaitTimeSeconds=5
        )

        if 'Messages' not in response:
            print("No new messages in the queue.")
            return

        for message in response['Messages']:
            body = eval(message['Body'])  # Convert string to dictionary
            username = body['username']
            book_id = body['book_id']
            borrow_date = body['borrow_date']

            # Process the borrow request
            book_response = books_table.get_item(Key={'book_id': book_id})
            print("Book_table", book_response)
            
            book_data = book_response.get('Item', {})
            print("book data:", book_data)

            if not book_data or int(book_data.get('quantity', '0')) <= 0:
                print(f"Book {book_id} is out of stock. Skipping request.")
                continue

            # Update the book's quantity
            new_quantity = int(book_data['quantity']) - 1
            print("New_quantity", new_quantity)
            books_table.update_item(
                Key={'book_id': book_id},
                UpdateExpression="SET quantity = :q",
                ExpressionAttributeValues={':q': str(new_quantity)}
            )

            # Calculate the due date using BookReturnCalculator
            book_return_calculator = BookReturnCalculator()
            due_date = book_return_calculator.calculate_due_date(borrow_date)
            print("Due_date:", due_date)

            # Insert borrow record into DynamoDB
            borrow_table.put_item(
                Item={
                    'username': username,
                    'book_id': book_id,
                    'borrow_date': borrow_date,
                    'due_date': due_date
                }
            )

            # Delete the processed message from SQS
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

            print(f"Processed borrow request for user {username}, book {book_id}.")

    except Exception as e:
        print("Error processing SQS messages:", str(e))


