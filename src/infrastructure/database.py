import os
from contextlib import contextmanager
from dataclasses import asdict
from typing import Optional, Any, List, TypeVar
from motor.motor_asyncio import AsyncIOMotorClient

T = TypeVar('T')

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None
    database_name = 'fantasy_back'
    test_database_name = 'fantasy_back_test'
    _current_db_name = database_name
    _connected = False
    
    @classmethod
    @contextmanager
    def using_database(cls, database_name: str):
        """Switch database context (for testing)"""
        original_name = cls._current_db_name
        cls._current_db_name = database_name
        if cls.client:
            cls.database = cls.client[cls._current_db_name]
        try:
            yield
        finally:
            cls._current_db_name = original_name
            if cls.client:
                cls.database = cls.client[cls._current_db_name]
    
    @classmethod
    async def connect(cls):
        """Initialize MongoDB connection"""
        if not cls._connected:
            mongo_host = os.getenv("MONGO_HOST", "fantasy_mongodb")
            mongo_uri = f"mongodb://fantasy:fantasy@{mongo_host}:27017/?authSource=admin"
            cls.client = AsyncIOMotorClient(mongo_uri)
            cls.database = cls.client[cls._current_db_name]
            cls._connected = True
            
    @classmethod
    async def disconnect(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            cls._connected = False

    @classmethod
    def _get_collection(cls, model_name: str):
        """Get collection for a model"""
        collection_map = {
            "User": "users",
            "Item": "items",
            "Store": "stores"
        }
        collection_name = collection_map.get(model_name, model_name.lower() + "s")
        return cls.database[collection_name]

    @classmethod
    async def clear(cls):
        """Clear all collections"""
        await cls.connect()
        collections = ["users", "items", "stores"]
        for collection_name in collections:
            await cls.database[collection_name].delete_many({})

    @classmethod
    async def get_obj(cls, model: T, id: str) -> T | None:
        """Get object by ID"""
        await cls.connect()
        collection = cls._get_collection(model.__name__)
        
        obj_data = await collection.find_one({"_id": id})
        if not obj_data:
            return None
        
        # Convert _id to id for dataclass
        obj_data["id"] = obj_data.pop("_id")
        
        # Use from_dict if available
        if hasattr(model, 'from_dict'):
            return model.from_dict(obj_data)
        
        return model(**obj_data)

    @classmethod
    async def get_all(cls, model: T) -> List[Any]:
        """Get all objects of a model type"""
        await cls.connect()
        collection = cls._get_collection(model.__name__)
        
        objects = []
        cursor = collection.find({})
        async for obj_data in cursor:
            obj_data["id"] = obj_data.pop("_id")
            objects.append(model(**obj_data))
        
        return objects

    @classmethod
    async def find_by_field(cls, model: T, field: str, value: Any) -> Optional[Any]:
        """Find object by field value"""
        await cls.connect()
        collection = cls._get_collection(model.__name__)
        
        obj_data = await collection.find_one({field: value})
        if not obj_data:
            return None
        
        obj_data["id"] = obj_data.pop("_id")
        
        return model(**obj_data)

    @classmethod
    async def save_obj(cls, obj: T):
        """Save or update object"""
        await cls.connect()
        model_type = type(obj).__name__
        collection = cls._get_collection(model_type)
        
        obj_dict = asdict(obj)
        obj_dict["_id"] = obj_dict.pop("id")
        
        await collection.replace_one(
            {"_id": obj_dict["_id"]},
            obj_dict,
            upsert=True,
        )
        
    @classmethod
    async def update_one(cls, model: T, filter_query: dict, update_query: dict):
        """Remove object"""
        await cls.connect()
        collection = cls._get_collection(model.__name__)

        return await collection.update_one(filter_query, update_query)

    @classmethod
    async def remove_obj(cls, obj: T):
        """Remove object"""
        await cls.connect()
        model_type = type(obj).__name__
        collection = cls._get_collection(model_type)
        
        await collection.delete_one({"_id": obj.id})

    @classmethod
    async def save_multiple_obj(cls, type: str, objs: dict):
        """Save multiple objects at once"""
        await cls.connect()
        collection = cls._get_collection(type)
        
        # Clear collection first
        await collection.delete_many({})
        
        # Insert all objects
        if objs:
            documents = []
            for obj_id, obj_data in objs.items():
                obj_data["_id"] = obj_id
                documents.append(obj_data)
            
            if documents:
                await collection.insert_many(documents)
                
                