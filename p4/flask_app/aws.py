# flask_app/aws.py

import boto3

s3_client = boto3.client("s3")

def upload_file(file):
    """
    Uploads a file object to S3 and returns its URL.
    Assumes file is a Werkzeug `FileStorage` object.
    """
    bucket_name = "your-bucket-name"  # change this!
    key = f"uploads/{file.filename}"
    
    s3_client.upload_fileobj(
        Fileobj=file,
        Bucket=bucket_name,
        Key=key,
        ExtraArgs={"ACL": "public-read"}  # optional
    )
    
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"
