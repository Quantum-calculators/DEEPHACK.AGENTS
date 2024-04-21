from dotenv import load_dotenv
import os

load_dotenv()


MONGODB_URL = os.environ.get("MONGODB_URL")
MONGODB_PORT = os.environ.get("MONGODB_PORT")
MONGODB_HOST = os.environ.get("MONGODB_HOST")
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MESSAGE_DB = os.environ.get("MESSAGE_DB")
MESSAGE_COLL = os.environ.get("MESSAGE_COLL")
USER_DB = os.environ.get("USER_DB")
USER_COLL = os.environ.get("USER_COLL")
