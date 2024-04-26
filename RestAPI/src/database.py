from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from config import (
    USER_DB,
    USER_COLL,
    MESSAGE_COLL,
    MESSAGE_DB,
    MONGODB_HOST,
    MONGODB_PORT,
)

MongoUrl = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"

client = {}


@asynccontextmanager
async def dbInit(app: FastAPI):
    print(MongoUrl)
    client["client"] = AsyncIOMotorClient(MongoUrl)
    client["MessageDB"] = (
        client["client"].get_database(MESSAGE_DB).get_collection(MESSAGE_COLL)
    )
    client["UserDB"] = client["client"].get_database(USER_DB).get_collection(USER_COLL)
    yield
    client["client"].close()
