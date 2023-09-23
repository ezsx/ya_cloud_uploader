from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

# import logging


class Settings(BaseSettings):
    API_KEY: str = Field("1234567abcdef", alias='API_KEY')
    API_KEY_NAME: str = Field("access_token", alias='API_KEY_NAME')
    AWS_ACCESS_KEY_ID: str = Field("XXX", alias='AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: str = Field("XXX", alias='AWS_SECRET_ACCESS_KEY')
    ENDPOINT_URL: str = Field("https://storage.yandexcloud.net", alias='ENDPOINT_URL')


config = Settings()


print(Settings().model_dump())
