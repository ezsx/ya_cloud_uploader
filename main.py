import logging
import os
from botocore.exceptions import ClientError

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.security.api_key import APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN

import boto3

API_KEY = "1234567abcdef"
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

app = FastAPI()


async def get_api_key(
        api_key_query: str = Depends(api_key_query),
):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.post("/upload", dependencies=[Depends(get_api_key)])
async def upload_audio(file: UploadFile = File(...)):
    os.makedirs('upload_files', exist_ok=True)
    with open(f"upload_files/{file.filename}", 'wb') as buffer:
        content = await file.read()  # Read file
        buffer.write(content)  # Write file to buffer
    upload_file_to_s3(file_name=f"upload_files/{file.filename}")
    return {"filename": file.filename, "detail": "File has been successfully downloaded."}

def create_connect_yc():
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id="XXX",
        aws_secret_access_key="XXX",
    )
    return s3

def upload_file_to_s3(file_name, bucket="conspectus-bucket", object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = create_connect_yc()
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
