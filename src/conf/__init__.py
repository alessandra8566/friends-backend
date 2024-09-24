import os
from dotenv import load_dotenv

if os.path.exists('.env.local'):
    load_dotenv('.env.local')
else:
    load_dotenv('.env')

# db
DB_CONNECT_STRING           = os.getenv("DB_CONNECT_STRING")

# api
API_SERVER_PORT             = 8000

# jwt
SECRET_KEY                  = os.getenv("JWT_SECRET_KET")
ALGORITHM                   = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
REFRESH_TOKEN_EXPIRE_DAYS   = 7

# minio
MINIO_ENDPOINT              = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY            = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY            = os.getenv("MINIO_SECRET_KEY")
MINIO_ROOT_USER             = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD         = os.getenv("MINIO_ROOT_PASSWORD")

