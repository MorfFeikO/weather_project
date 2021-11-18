import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()


def get_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )


def get_resource():
    return boto3.resource(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )


def get_bucket_name():
    return os.getenv('AWS_BUCKET_NAME')


def upload_data_to_file(filename, content):
    s3_resource = get_resource()
    bucket = get_bucket_name()
    s3_resource.Object(bucket, filename).put(Body=content)


def get_files_list():
    files_list = []
    s3_client = get_client()
    bucket = get_bucket_name()
    for item in s3_client.list_objects(Bucket=bucket)['Contents']:
        files_list.append(item['Key'])
    return files_list


def download_data_from_file(filename):
    s3_client = get_client()
    bucket = get_bucket_name()

    for obj in s3_client.list_objects(Bucket=bucket)['Contents']:
        if obj['Key'] == filename:
            data = s3_client.get_object(Bucket=bucket, Key=filename)
            content = data['Body'].read()
            return json.loads(content)
