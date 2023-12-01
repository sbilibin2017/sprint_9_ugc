from enum import Enum
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic.fields import Field
from pydantic_settings import BaseSettings

logging_config.dictConfig(LOGGING)
load_dotenv(".env")


class MongoSettings(BaseSettings):
    class Config:
        env_prefix = "mongo_"

    host: str = Field("localhost", env="host")
    port: int = Field(27017, env="port")
    user: str = Field(..., env="user")
    password: str = Field(..., env="password")
    db_name: str = Field(..., env="db_name")
    collection_name: str = Field(..., env="collection_name")
    use_index: str = Field("false", env="use_index")

    @field_validator("use_index")
    @classmethod
    def validate_use_mongo_index(cls, v):
        return v.lower() == "true"


class ElasticSettings(BaseSettings):
    class Config:
        env_prefix = "elastic_"

    host: str = Field("localhost", env="host")
    port: int = Field(9200, env="port")
    index_name: str = Field("events", env="index_name")


class Settings(BaseSettings):
    CHUNK_SIZE: int = Field(1000, env="CHUNK_SIZE")
    FILLING_SIZE: int = Field(1000, env="FILLING_SIZE")

    mongo: MongoSettings = Field(default_factory=MongoSettings)
    elastic: ElasticSettings = Field(default_factory=ElasticSettings)

    update_limit: int = Field(1000, env="LIMIT_SIZE_ON_UPDATE")


class OlapProviders(str, Enum):
    MONGODB = "mongodb"
    ELASTIC = "elastic"


def get_olap_providers():
    from data_management.clients.elastic import ElasticsearchClient
    from data_management.clients.mongodb import MongoClient

    providers = {
        OlapProviders.MONGODB: MongoClient,
        OlapProviders.ELASTIC: ElasticsearchClient,
    }

    return providers


settings = Settings()
