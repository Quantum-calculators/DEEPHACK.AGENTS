from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.environ.get("MONGODB_URL")

MESSAGE_DB = os.environ.get("MESSAGE_DB")
MESSAGE_COLL = os.environ.get("MESSAGE_COLL")
USER_DB = os.environ.get("USER_DB")
USER_COLL = os.environ.get("USER_COLL")
