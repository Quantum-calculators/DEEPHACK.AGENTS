from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.environ.get("MONGODB_URL")
DB1_NAME = os.environ.get("DB1_NAME")
DB1_COLL = os.environ.get("DB1_COLL")
