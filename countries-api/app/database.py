from motor.motor_asyncio import AsyncIOMotorClient
import os
from bson import ObjectId
from typing import Dict, Any, List

# MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
database = client.countries_db
country_collection = database.get_collection("countries")


# Add function to handle MongoDB document serialization
def convert_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MongoDB document to JSON serializable dictionary. This function converts ObjectId fields to strings and recursively processes nested dictionaries and lists to ensure they are JSON serializable.

    Args:
        doc (Dict[str, Any]): The MongoDB document to convert.

    Returns:
        Dict[str, Any]: The converted document with ObjectId fields as strings.

    If the input document is None, it returns None.
    """
    if doc is None:
        return None

    # Convert ObjectId to string
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])

    # Recursively process nested dictionaries and arrays
    for key, value in doc.items():
        # Convert ObjectId in nested dictionaries
        if isinstance(value, dict):
            doc[key] = convert_mongo_doc(value)
        # Convert ObjectId in lists of dictionaries
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            doc[key] = [convert_mongo_doc(item) for item in value]

    return doc



