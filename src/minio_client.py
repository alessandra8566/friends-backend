from minio import Minio
from minio.error import S3Error
import conf

class MinioClient:
    def __init__(self):
        self.client = Minio(
            conf.MINIO_ENDPOINT,
            access_key=conf.MINIO_ROOT_USER,
            secret_key=conf.MINIO_ROOT_PASSWORD,
            secure=False,  # Set to True if using HTTPS
        )

    def upload_file(self, bucket_name, object_name, data, file_size):
        try:
            # Check if the bucket exists
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)

            # Upload the file
            self.client.put_object(bucket_name, object_name, data, file_size)
            return True
        except S3Error as err:
            print(f"Error: {err}")
            return False

    def list_buckets(self):
        return self.client.list_buckets()