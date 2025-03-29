from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings
import boto3

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cover_image = models.ImageField(upload_to='book_covers/')
    quantity = models.IntegerField(default=1)  # Corrected field type
    return_due_date = models.DateField(null=True, blank=True)  # New field for return due date

    def save(self, *args, **kwargs):
        # Save to Django DB first (to get the book_id)
        super().save(*args, **kwargs)

        # Now that book_id is available, proceed with uploading to DynamoDB
        if self.cover_image:
            # Upload the image to S3 if it exists
            file_path = default_storage.save(self.cover_image.name, self.cover_image)
            s3_url = default_storage.url(file_path)
            print(s3_url)
            # Store only the URL of the image in DynamoDB
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('Book')
            print(dynamodb)
            table.put_item(
                Item={
                    'book_id': str(self.book_id),  # book_id as string
                    'title': self.title,
                    'author': self.author,
                    'price': str(self.price),  # Convert Decimal to String
                    'book_img': str(s3_url),
                    'quantity': int(self.quantity),  # Convert to int
                    'return_due_date': str(self.return_due_date),  # Store return_due_date as a string
                    # Store S3 URL in DynamoDB
                }
            )

    def delete(self, *args, **kwargs):
        """Delete book from DynamoDB when deleting in Django."""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Books')

        table.delete_item(Key={'book_id': str(self.book_id)})
        super().delete(*args, **kwargs)  # Delete from Django DB

    @staticmethod
    def get_all_books():
        """Retrieve all books from DynamoDB."""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Books')

        response = table.scan()
        return response.get('Items', [])

    @staticmethod
    def get_book_by_id(book_id):
        """Retrieve a book by ID from DynamoDB."""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Books')

        response = table.get_item(Key={'book_id': str(book_id)})
        return response.get('Item', {})

    def __str__(self):
        return self.title
        
    def book_img_url(self):
        """Retrieve book image URL from DynamoDB."""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Book')

        response = table.get_item(Key={'book_id': str(self.book_id)})
        item = response.get('Item')
        if item and 'book_img' in item:
            return item['book_img']
        return "No Image"

    def __str__(self):
        return self.title




