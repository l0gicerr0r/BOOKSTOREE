# BOOKSTOREE
CLOUD_PLATFORM_PROJECT
Dependencies:

Python (Ensure Python 3.x is installed)

Django (Latest stable version)

AWS SDK (Boto3) for AWS service interactions

Django REST Framework for API development

SQLite / AWS DynamoDB (for database storage)

AWS S3 (for storing media files like book covers)

AWS SNS & SQS (for notifications and message queueing)

AWS Lambda (for background tasks)

Git & GitHub Actions (for CI/CD pipeline setup)

Docker (Optional, for containerization)

Deployment Steps:

1. Clone the Repository:

git clone <repository_url>
cd <project_directory>

2. Create and Activate Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

3. Install Dependencies:

pip install -r requirements.txt

4. Set Up Environment Variables:

Create a .env file and add the necessary AWS credentials and settings:

AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_REGION=<your-region>
DATABASE_URL=<your-database-url>
S3_BUCKET_NAME=<your-s3-bucket>
SNS_TOPIC_ARN=<your-sns-topic-arn>
SQS_QUEUE_URL=<your-sqs-queue-url>

5. Apply Database Migrations:

python manage.py migrate

6. Run the Development Server:

python manage.py runserver

7. Configure CI/CD Pipeline:

Ensure .github/workflows/deploy.yml is correctly configured for GitHub Actions.

Push the code to GitHub to trigger the pipeline.

8. Deploy to AWS Elastic Beanstalk:

egit init
egit add .
egit commit -m "Initial commit"
egit push origin main
eb init -p python-3.x <app-name>
eb create <environment-name>

9. Monitor Logs and Errors:

eb logs

10. Verify the Deployment:

Visit the Elastic Beanstalk URL to check the deployed application.

Ensure all AWS services are properly integrated.

Configuration Files:

.env (Environment variables for AWS & database settings)

settings.py (Django configurations including AWS & DB settings)

requirements.txt (Python dependencies)

.github/workflows/deploy.yml (CI/CD pipeline setup for GitHub Actions)

Dockerfile (If containerizing the application)
