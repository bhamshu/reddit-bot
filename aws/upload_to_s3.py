import boto3
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variables as usual
access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
default_region = os.getenv('AWS_DEFAULT_REGION')

def upload_image_to_s3(image, custom_name, bucket_name):
    # Save the image locally with the custom name
    image_path = f"{custom_name}.png"
    # image.save(image_path)
    
    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=default_region
    )

    
    # Upload the image to S3 with the custom name
    s3.upload_file(image, bucket_name, image_path)
    
    # Generate the URL of the uploaded image
    image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_path}"
    
    return image_url