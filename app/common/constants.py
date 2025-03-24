from datetime import timedelta
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=".env")

DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING", "mysql+pymysql://user:password@localhost:3306/db")
DB_HOST = getenv("DB_HOST", "localhost")
DB_USER = getenv("DB_USER", "user")
DB_PASSWORD = getenv("DB_PASSWORD", "password")
DB_NAME = getenv("DB_NAME", "db")

AWS_S3_ACCESS_KEY = getenv("AWS_S3_ACCESS_KEY", "AWS_S3_ACCESS_KEY")
AWS_S3_PRIVATE_KEY = getenv("AWS_S3_PRIVATE_KEY", "AWS_S3_PRIVATE_KEY")
REGION_NAME = getenv("REGION_NAME", "REGION_NAME")
BUCKET_NAME = getenv("BUCKET_NAME", "BUCKET_NAME")

HASH_SALT = getenv("HASH_SALT", "SomeRandomStringHere")

COOKIES_KEY_NAME = "session_token"
SESSION_TIME = timedelta(days=30)