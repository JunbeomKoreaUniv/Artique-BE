import boto3
from flask import current_app
from werkzeug.utils import secure_filename
import os
import uuid


def upload_file_to_s3(file, bucket_name, folder=""):
    # S3 클라이언트 생성
    s3 = boto3.client(
        "s3",
        aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
        region_name=current_app.config["AWS_REGION"]
    )

    # 파일명 지정
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{folder}/{uuid.uuid4().hex}{file_extension}"

    # 파일 업로드
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            unique_filename,
            ExtraArgs={
                "ACL": "public-read",  # 공개 URL을 통해 접근 가능하도록 설정
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

    # 파일 URL 생성
    file_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{unique_filename}"
    return file_url
