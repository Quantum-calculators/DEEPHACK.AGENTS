from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_async_mongo_session
from Name.schemas import RequestText, ResponseText
from fastapi import status

from config import DB1_NAME, DB1_COLL


route = APIRouter(prefix="/Name", tags=["Name"])


@route.post(
    "/set-token", response_model=ResponseText, status_code=status.HTTP_201_CREATED
)
async def set_token(
    req: RequestText,
    session: AsyncIOMotorClient = Depends(get_async_mongo_session),
):
    database = session.get_database(DB1_NAME).get_collection(DB1_COLL)
    await database.insert_one({"Param1": "Arg1"})
    async for elem in database.find():
        print(elem)
    await database.delete_one({"Param1": "Arg1"})
    return ResponseText(text="Da")
