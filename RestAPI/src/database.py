from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_URL, USER_DB, USER_COLL, MESSAGE_COLL, MESSAGE_DB

client = AsyncIOMotorClient(MONGODB_URL)

UserDB = client.get_database(USER_DB).get_collection(USER_COLL)
MessageDB = client.get_database(MESSAGE_DB).get_collection(MESSAGE_COLL)
