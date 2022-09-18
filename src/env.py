"""
Env module
~~~~~~~~~~~~~~~~~~~~~

This module initializes common configuration from environment variables
"""
import os
from dotenv import load_dotenv
from src.db import get_pymssql_url, get_snowflake_url

WORK_ENV=os.getenv("WORK_ENV") if os.getenv("WORK_ENV") else "dev"
WORK_DIR = os.getenv("WORK_DIR") if os.getenv("WORK_DIR") else "/workspace"

# load .env file on dev machine
if WORK_ENV == "dev":
    env_file=os.path.join(WORK_DIR, ".env")
    if os.path.exists(env_file):
        load_dotenv(dotenv_path = env_file, verbose=True)

# work dirs

TEMP_DIR = os.path.join(WORK_DIR,'.tmp') # temporary files
DATA_DIR = os.path.join(WORK_DIR,".data") # data
BUILD_DIR = os.path.join(WORK_DIR,".build") # build


# source - bigdb
SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_USER_ID=os.getenv("SPOTIFY_USER_ID")


SNOWFLAKE_ACCOUNT=os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_REGION=os.getenv("SNOWFLAKE_REGION")
SNOWFLAKE_CLOUD=os.getenv("SNOWFLAKE_CLOUD")
# https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-account-locator
SNOWFLAKE_ACCOUNT_LOCATOR=f"{SNOWFLAKE_ACCOUNT}.{SNOWFLAKE_REGION}.{SNOWFLAKE_CLOUD}"
SNOWFLAKE_URL=f"http://{SNOWFLAKE_ACCOUNT}.{SNOWFLAKE_REGION}.snowflakecomputing.com"

# snowflake dbt setup
SNOWFLAKE_ROLE=os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_DATABASE=os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_WAREHOUSE=os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_TRANSFORM_SCHEMA=os.getenv("SNOWFLAKE_TRANSFORM_SCHEMA")
SNOWFLAKE_RAW_SCHEMA=os.getenv("SNOWFLAKE_RAW_SCHEMA")


# snowflake credentials
SNOWFLAKE_USER=os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD=os.getenv("SNOWFLAKE_PASSWORD")

TARGET_DB_URL = get_snowflake_url(
        SNOWFLAKE_ACCOUNT_LOCATOR,
        SNOWFLAKE_USER,
        SNOWFLAKE_PASSWORD,
        SNOWFLAKE_DATABASE,
        SNOWFLAKE_RAW_SCHEMA,
        SNOWFLAKE_WAREHOUSE,
        SNOWFLAKE_ROLE
)
