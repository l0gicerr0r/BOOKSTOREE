
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .queue_handler import send_borrow_request_to_queue, process_borrow_requests_from_queue
from .forms import LoginForm, RegisterForm
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.contrib import messages
from boto3.dynamodb.conditions import Key
from django.conf import settings
from django.contrib import messages 
from bookreturncalculatorPkg.bookreturncalculator import BookReturnCalculator







# Initialize AWS DynamoDB
region = 'us-east-1'  # Update if needed
dynamodb = boto3.resource('dynamodb', region_name=region)

# Ensure that these tables exist in DynamoDB
users_table = dynamodb.Table('Users')
books_table = dynamodb.Table('Book')  # Admins add books here

# ---------------------------
# LANDING PAGE
# ---------------------------
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('user_home')  # Redirect to book listing page
    return render(request, 'accounts/landing.html')  # Show landing page

# ---------------------------
# HOME PAGE (Only logged-in users can see this)
# ---------------------------
@login_required
def home(request):
    return render(request, 'accounts/home.html')

#---------------------------
#USER PROFILE PAGE
#---------------------------
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

#---------------------------
#USER REGISTRATION (Sign Up)
#---------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Store user data in DynamoDB
            try:
                users_table.put_item(
                    Item={
                        'username': user.username,
                        'email': user.email if user.email else "N/A",
                        'borrowed_books': []  # Initialize empty borrowed books list
                    }
                )
            except (NoCredentialsError, PartialCredentialsError) as e:
                print("AWS Credentials Error:", str(e))

            login(request, user)
            return redirect('user_home')
        else:
            print(form.errors)  # Debugging: Print form errors in the terminal
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})





# ---------------------------
# USER LOGIN
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# ---------------------------
# USER LOGOUT
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------------
# DISPLAY BOOKS & USER'S BORROWED BOOKS
# ---------------------------
@login_required
def user_home(request):
    try:
        # Fetch all available books from DynamoDB
        response = books_table.scan()
        books = response.get('Items', [])

        # Fetch user's borrowed books from Users table in DynamoDB
        user_response = users_table.get_item(Key={'username': request.user.username})
        user_data = user_response.get('Item', {})

        borrowed_books = user_data.get('borrowed_books', [])  # Default to empty list if no borrowed books

        # Calculate remaining days for borrowed books
        today = datetime.today()
        for book in borrowed_books:
            borrow_date = datetime.strptime(book['borrow_date'], '%Y-%m-%d')
            due_date = borrow_date + timedelta(days=30)
            book['days_left'] = (due_date - today).days
            book['due_date'] = due_date.strftime('%Y-%m-%d')  # Format due date

   
    except Exception as e:
        print("Error fetching books:", str(e))
        books, borrowed_books = [], []
    
    return render(request, 'accounts/user_home.html', {
        'books': books,
        'borrowed_books': borrowed_books
    })




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




#fffffffffffffffffffffffff



@login_required
def borrow_book(request, book_id):
    if request.method == "POST":
        try:
            username = request.user.username

            # Fetch user data from DynamoDB
            user_response = users_table.get_item(Key={'username': username})
            user_data = user_response.get('Item', {})

            if not user_data:
                messages.error(request, "User not found.")
                return redirect('user_home')

            # Fetch the book details from DynamoDB
            book_response = books_table.get_item(Key={'book_id': book_id})
            book_data = book_response.get('Item', {})

            if not book_data:
                messages.error(request, "Book not found.")
                return redirect('user_home')

            # Convert book quantity to integer safely
            book_quantity = int(book_data.get('quantity', '0'))
            if book_quantity <= 0:
                messages.error(request, "This book is currently out of stock.")
                return redirect('user_home')

            # Query Borrow table for all books borrowed by this user
            borrowed_response = borrow_table.query(
                KeyConditionExpression=Key('username').eq(username)
            )
            borrowed_books = borrowed_response.get('Items', [])

            # Check if user has reached maximum borrow limit (5 books)
            if len(borrowed_books) >= 5:
                messages.error(request, "You have reached the maximum borrow limit of 5 books.")
                return redirect('user_home')

            # Check if user already has this book borrowed
            if any(book["book_id"] == book_id for book in borrowed_books):
                messages.error(request, "You already have this book borrowed.")
                return redirect('user_home')

            # ✅ Calculate Due Date using BookReturnCalculator
            calculator = BookReturnCalculator()
            borrow_date = datetime.utcnow().strftime("%Y-%m-%d")  # Borrow date (today)
            due_date = calculator.calculate_due_date(borrow_date)  # Calculate due date

            print("Sending SQS with due date:", due_date)

            # Send the borrow request to SQS (Include due_date)
            send_borrow_request_to_queue(username, book_id, due_date)

            messages.success(request, "Your borrow request has been sent for processing.")

            # Process SQS queue (optional, if you process requests immediately)
            process_borrow_requests_from_queue()

            messages.success(request, "Your borrow request has been processed.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('user_home')




# ---------------------------
# NEW FUNCTION: DISPLAY ONLY THE NAMES OF BORROWED BOOKS
# ---------------------------








