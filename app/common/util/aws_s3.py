import boto3

from common.constants import AWS_S3_ACCESS_KEY, AWS_S3_PRIVATE_KEY, REGION_NAME, BUCKET_NAME

s3_client = boto3.client(
    "s3", region_name=REGION_NAME, aws_access_key_id=AWS_S3_ACCESS_KEY, aws_secret_access_key=AWS_S3_PRIVATE_KEY
)

def upload_file_on_s3(file_key: str, file_bytes):
    try:
        s3_client.upload_fileobj(file_bytes, BUCKET_NAME, file_key)
    except Exception as er:
        print(str(er))
        return None

    return f"https://s3-{BUCKET_NAME}.amazonaws.com/{file_key}"

def create_presigned_url(file_key: str, fields=None, conditions=None):
    try:
        if fields is None:
            fields = {
                "Content-Type": "image/jpeg",  # 필요에 따라 적절한 Content-Type 설정
            }
        
        if conditions is None:
            conditions = [
                {"Content-Type": "image/jpeg"},
                ["content-length-range", 1, 104857600],  # 1 Byte ~ 100 MB
            ]

        response = s3_client.generate_presigned_post(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=3600
        )
    except Exception as er:
        print(str(er))
        return None

    """
    presignedPostData = {
        "url": "https://s3-{BUCKET_NAME}.amazonaws.com/",
        "fields": {
            "key": response["fields"]["key"],
            "AWSAccessKeyId": response["fields"]["AWSAccessKeyId"],
            "policy": response["fields"]["policy"],
            "signature": response["fields"]["signature"],
            "Content-Type": "image/jpeg",
        }
    };
    """
    return response