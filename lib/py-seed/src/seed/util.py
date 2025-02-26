import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker
import functools
import os

async def insert_user(collection, fake, index):
    """Async function to insert a single person document into MongoDB"""
    name = fake.name()
    await collection.insert_one({"name": name})
    print(f"- created name: {name}")
    return name

async def seed(connection_string: str, count: int):
    # Connect to MongoDB using Motor's async driver
    client = AsyncIOMotorClient(connection_string)
    db = client.demo
    collection = db.users

    # Initialize Faker
    fake = Faker()

    # Create tasks for all inserts
    tasks = [insert_user(collection, fake, i) for i in range(count)]

    # Gather and execute all tasks concurrently
    results = await asyncio.gather(*tasks)

    print(f"Successfully inserted {len(results)} documents")
    client.close()



def with_connection_string(db_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(count, *args, **kwargs):
            if db_type == 'mongodb':
                connection_string = os.getenv("MONGODB_CONNECTION_STRING", "")
            elif db_type == 'docdb':
                connection_string = f"{os.getenv('DOCDB_CONNECTION_STRING', '')}&tlsCAFile=global-bundle.pem"
            else:
                raise ValueError(f"Unsupported database type: {db_type}")

            return func(connection_string, count, *args, **kwargs)
        return wrapper
    return decorator
