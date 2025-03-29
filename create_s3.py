import boto3

# Set your bucket name (MUST be globally unique)
BUCKET_NAME = "my-bookstore-bucket-12345"  # Change this to a unique name

# Connect to S3
s3 = boto3.client("s3")

# Get the AWS region
session = boto3.session.Session()
current_region = session.region_name  # Get the current AWS region

# Check if the region is us-east-1
if current_region == "us-east-1":
    # Create bucket without LocationConstraint
    s3.create_bucket(Bucket=BUCKET_NAME)
else:
    # Create bucket with LocationConstraint for other regions
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": current_region},
    )

print(f"S3 bucket '{BUCKET_NAME}' created successfully in region {current_region}!")
