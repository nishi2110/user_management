import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
)


def upload_to_minio(file_path: str, bucket_name: str, object_name: str) -> str:
    s3_client.upload_file(file_path, bucket_name, object_name)
    return f"{os.getenv('MINIO_ENDPOINT')}/{bucket_name}/{object_name}"
