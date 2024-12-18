from minio import Minio
import os

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

def upload_file(bucket_name, object_name, file_path):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    client.fput_object(bucket_name, object_name, file_path)

def get_file(bucket_name, object_name):
    return client.get_object(bucket_name, object_name)