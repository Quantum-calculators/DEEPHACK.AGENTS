import motor.motor_asyncio
import asyncio

MONGO_DETAILS = "mongodb://localhost:27017"
session = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = session.get_database("TestDB")


async def main():
    database_col1 = database.get_collection("Bebra")
    await database_col1.insert_one({"test": "yes"})
    async for elem in database_col1.find():
        print(elem)
    await database_col1.delete_one({"test": "yes"})


if __name__ == "__main__":
    asyncio.run(main=main())
