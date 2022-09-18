"""
Env module
~~~~~~~~~~~~~~~~~~~~~

This module initializes common configuration from environment variables
"""
import os
from dotenv import load_dotenv
from src.db import get_pymssql_url

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


# source - spotify
SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_USER_ID=os.getenv("SPOTIFY_USER_ID")

# Postgres
PG_HOST=os.getenv("PG_HOST")
PG_USER=os.getenv("PG_USER")
PG_PWD=os.getenv("PG_PWD")
PG_DATABASE=os.getenv("PG_DATABASE")
PG_SCHEMA=os.getenv("PG_SCHEMA")
PG_PORT=os.getenv("PG_PORT")


