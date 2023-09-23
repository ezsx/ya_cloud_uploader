import logging

import os
from botocore.exceptions import ClientError

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import boto3

from config import config

logging.basicConfig(level=logging.DEBUG)

api_key_header = APIKeyHeader(name=config.API_KEY_NAME, auto_error=False)
app = FastAPI()


async def get_api_key(
        api_key_header: str = Depends(api_key_header),
):
    if api_key_header == config.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.post("/upload", dependencies=[Depends(get_api_key)])
async def upload_audio(file: UploadFile = File(...)):
    file_name = f"upload_files/{file.filename}"
    os.makedirs('upload_files', exist_ok=True)
    with open(file_name, 'wb') as buffer:
        content = await file.read()  # Read file
        buffer.write(content)  # Write file to buffer
    upload_file_to_s3(file_name=file_name)
    os.remove(file_name)
    return {"filename": file_name, "detail": "File has been successfully downloaded."}


def create_connect_yc():
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=config.ENDPOINT_URL,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )
    return s3


def upload_file_to_s3(file_name, bucket="conspectus-bucket", object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = create_connect_yc()
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True
