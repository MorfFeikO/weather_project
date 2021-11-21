"""
Operations with AWS s3 bucket.
...
Functions:
    upload_data_to_file(data)
        Upload data to file on s3 AWS bucket.

    get_files_list()
        Get list of files on s3 AWS bucket.

    download_data_from_file()
        Download data from file on s3 AWS bucket.
"""
import asyncio
import os
import json
import boto3
import time
import concurrent.futures
import functools

from dotenv import load_dotenv
from app.models import FreshWeather

load_dotenv()

executor = concurrent.futures.ThreadPoolExecutor()


def aio(f):
    async def aio_wrapper(*args, **kwargs):
        f_bound = functools.partial(f, **kwargs)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, f_bound(*args))
    return aio_wrapper


def get_client():
    """Get client connection to AWS s3 bucket."""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )


def get_resource():
    """Get resource connection to AWS s3 bucket."""
    return boto3.resource(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )


def get_bucket_name():
    """Get bucket name of AWS s3 bucket containing data."""
    return os.getenv('AWS_BUCKET_NAME')


def upload_data_to_file(filename, content):
    """Upload data to file on s3 AWS bucket.
    ...
    :param filename: str
        Name of file upload data to.
    :param content: str
        Content of file in json representation.
    """
    s3_resource = get_resource()
    bucket = get_bucket_name()
    s3_resource.Object(bucket, filename).put(Body=content)


def get_files_list():
    """Get list of files on s3 AWS bucket.
    ...
    :return files_list: list
        List of str filenames in AWS s3 bucket.
    """
    files_list = []
    s3_client = get_client()
    bucket = get_bucket_name()
    for item in s3_client.list_objects(Bucket=bucket)['Contents']:  # TODO: if empty KeyError
        files_list.append(item['Key'])
    return files_list


def download_data_from_file(filename):
    """Download data from file on s3 AWS bucket.
    ...
    :param filename: str
        Name of file upload data from.
    :return dict
        Content of file.
    """
    s3_client = get_client()
    bucket = get_bucket_name()

    for obj in s3_client.list_objects(Bucket=bucket)['Contents']:
        if obj['Key'] == filename:
            data = s3_client.get_object(Bucket=bucket, Key=filename)
            content = data['Body'].read()
            return json.loads(content)
##################################################################


async def get_files_list_async():
    """Get list of files on s3 AWS bucket.
    ...
    :return files_list: list
        List of str filenames in AWS s3 bucket.
    """
    files_list = []
    s3_client = await get_client_async()
    bucket = get_bucket_name()
    for item in s3_client.list_objects(Bucket=bucket)['Contents']:  # TODO: if empty KeyError
        files_list.append(item['Key'])
    return files_list


async def get_client_async():
    """Get client connection to AWS s3 bucket."""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )


async def get_bucket_list_async():
    start = time.time()
    s3_client = await get_client_async()
    bucket = get_bucket_name()
    bucket_list = s3_client.list_objects(Bucket=bucket)['Contents']
    print('func - ', time.time() - start)
    return bucket_list


async def download_data_from_file_async(filename, bucket_list):
    """Download data from file on s3 AWS bucket.
    ...
    :param filename: str
        Name of file upload data from.
    :return dict
        Content of file.
    """
    start = time.time()
    s3_client = await get_client_async()
    bucket = get_bucket_name()

    # bucket_list = s3_client.list_objects(Bucket=bucket)['Contents']

    for obj in bucket_list:
        if obj['Key'] == filename:

            s1 = time.time()
            data = s3_client.get_object(Bucket=bucket, Key=filename)  # this line 0,14/0,57 sec
            print('bucket_list', time.time() - s1)

            content = data['Body'].read()
            json_content = json.loads(content)
            weather = FreshWeather(
                json_content['country'],
                json_content['city'],
                json_content['temperature'],
                json_content['condition'])

            print('END of getting filedata', time.time() - start)
            return weather

@aio
async def ooo(filename):
    start = time.time()
    s3_client = get_client()
    bucket = get_bucket_name()
    # download_file = aio(s3_client.download_file)
    # await download_file(bucket, filename, filename)
    await s3_client.download_file(bucket, filename, filename)
    print('inner time', time.time() - start)


async def gogogo(files_list):
    start = time.time()
    tasks = []
    for filename in files_list:
        await ooo(filename)


    print('outer time', time.time() - start)


# asyncio.run(gogogo(get_files_list()))
