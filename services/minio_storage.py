# services/minio_client.py

from minio import Minio
from django.conf import settings
from minio.error import S3Error

minio_host = settings.MINIO_STORAGE_ENDPOINT
minio_access_key = settings.MINIO_STORAGE_ACCESS_KEY
minio_secret_key = settings.MINIO_STORAGE_SECRET_KEY
bucket_name = settings.MINIO_STORAGE_BUCKET_NAME


minio_client = Minio(minio_host, access_key=minio_access_key, secret_key=minio_secret_key, secure=False)


def upload_file_to_minio(file, file_name):
    try:
        # Ensure the bucket exists, create if it doesn't
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        # Upload the file
        minio_client.put_object(bucket_name, file_name, file, length=file.size)

        # Retrieve and print object details (optional)
        response = minio_client.get_object(bucket_name, file_name)
        return True
    except S3Error as e:
        print("S3Error occurred:", e)
        return False
    except Exception as e:
        print("Exception occurred:", e)
        return False


def download_from_minio(filepath):
    try:
        # Get the file from MinIO
        file_object = minio_client.get_object(bucket_name, filepath)
        return file_object
    except Exception as e:
        print("exception occur", e)
        return None
