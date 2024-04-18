from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_URL

async def get_async_mongo_session() -> AsyncGenerator[AsyncIOMotorClient, None]:
    async with AsyncIOMotorClient(MONGODB_URL) as session:
        yield session
