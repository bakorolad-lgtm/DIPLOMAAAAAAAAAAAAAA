import boto3
from botocore.config import Config


class S3Client:
    BOTO_CONFIG = Config(
        signature_version="s3v4",
        connect_timeout=10,
        read_timeout=10,
        # retries={"max_attempts": 5},
        tcp_keepalive=True,
    )
    def __init__(self, bucket: str):
        self._client = boto3.client(
            service_name="s3",
            config=self.BOTO_CONFIG,
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            endpoint_url="http://minio-files:9000",
            region_name="ru-central1",
        )
        self._bucket = bucket

        if not self._is_bucket_exists():
            raise self._create_bucket_if_not_exists()

    def _is_bucket_exists(self):
        try:
            self._client.head_bucket(Bucket=self._bucket)
            return True
        except Exception as e:
            print(e)
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                return False

            raise e

    def _create_bucket_if_not_exists(self):
        self._client.create_bucket(
            Bucket=self._bucket,
            CreateBucketConfiguration={
                "LocationConstraint": self._client.meta.region_name
            },
        )

    def upload_file(self, file, file_name):
        self._client.upload_fileobj(file, self._bucket, file_name)
