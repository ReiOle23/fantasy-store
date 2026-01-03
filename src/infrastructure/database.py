import json
import os
from contextlib import contextmanager
from dataclasses import asdict
from typing import Optional, Any

class Database:
	database_url = 'src/infrastructure/config/'
	database_file = 'database.json'

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
	def get_obj(cls, model_type: str, id: int) -> Any:
		cls._ensure_file_exists()
		with open(cls.database_url + cls.database_file, "r") as json_file:
			data = json.load(json_file)
		return data[model_type][str(id)]

	@classmethod
	def find_by_field(cls, model_type: str, field: str, value: Any) -> Optional[dict]:
		cls._ensure_file_exists()
		with open(cls.database_url + cls.database_file, "r") as json_file:
			data = json.load(json_file)
		for obj in data.get(model_type, {}).values():
			if obj.get(field) == value:
				return obj
		return None

	@classmethod
	def save_obj(cls, obj):
		cls._ensure_file_exists()
		model_type = type(obj).__name__
		with open(cls.database_url + cls.database_file, "r") as json_file:
			data = json.load(json_file)	
		data[model_type][str(obj.id)] = asdict(obj)
		with open(cls.database_url + cls.database_file, 'w') as json_file:
			json.dump(data, json_file, indent=4)
