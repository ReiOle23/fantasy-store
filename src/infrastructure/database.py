import json, os, threading
from contextlib import contextmanager
from dataclasses import asdict
from typing import Optional, Any, List, TypeVar

T = TypeVar('T')

class Database:
	database_url = 'src/infrastructure/config/'
	database_file = 'database.json'
	_lock = threading.Lock()

	@classmethod
	@contextmanager
	def using_database(cls, filename: str):
		original_file = cls.database_file
		cls.database_file = filename
		try:
			yield
		finally:
			cls.database_file = original_file

	@classmethod
	def _ensure_file_exists(cls):
		if not os.path.exists(cls.database_url + cls.database_file):
			cls.clear()

	@classmethod
	def clear(cls):
		with open(cls.database_url + cls.database_file, "w") as json_file:
			data = {
				"User": {},
				"Item": {},
				"Store": {}
			}
			json.dump(data, json_file, indent=4)

	@classmethod
	def get_obj(cls, model: T, id: int) -> Any:
		with cls._lock:
			cls._ensure_file_exists()
			with open(cls.database_url + cls.database_file, "r") as json_file:
				data = json.load(json_file)
			obj_data = data.get(model.__name__, {}).get(str(id))
			if not obj_data:
				return None
			if model.__name__ == "Item" and "owner" in obj_data and obj_data["owner"] is not None:
				if isinstance(obj_data["owner"], dict):
					from src.domain.entities.user import User
					obj_data["owner"] = User(**obj_data["owner"])
			
			return model(**obj_data)

	@classmethod
	def get_all(cls, model: T) -> List[dict]:
		with cls._lock:
			cls._ensure_file_exists()
			with open(cls.database_url + cls.database_file, "r") as json_file:
				data = json.load(json_file)
			return list(model(**obj) for obj in data.get(model.__name__, {}).values())
	
	@classmethod
	def find_by_field(cls, model: T, field: str, value: Any) -> Optional[dict]:
		with cls._lock:
			cls._ensure_file_exists()
			with open(cls.database_url + cls.database_file, "r") as json_file:
				data = json.load(json_file)
			for obj in data.get(model.__name__, {}).values():
				if obj.get(field) == value:
					return model(**obj)
			return None

	@classmethod
	def save_obj(cls, obj: T):
		with cls._lock:
			cls._ensure_file_exists()
			model_type = type(obj).__name__
			with open(cls.database_url + cls.database_file, "r") as json_file:
				data = json.load(json_file)
			data[model_type][str(obj.id)] = asdict(obj)
			with open(cls.database_url + cls.database_file, 'w') as json_file:
				json.dump(data, json_file, indent=4)

	@classmethod
	def save_multiple_obj(cls, type: str, objs: dict[dict]):
		with cls._lock:
			cls._ensure_file_exists()
			with open(cls.database_url + cls.database_file, "r") as json_file:
				data = json.load(json_file)
			data[type] = objs
			with open(cls.database_url + cls.database_file, 'w') as json_file:
				json.dump(data, json_file, indent=4)
    