from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not set in .env file")

client = AsyncIOMotorClient(MONGO_URI)
db = client["beyblade"]  # Database name
