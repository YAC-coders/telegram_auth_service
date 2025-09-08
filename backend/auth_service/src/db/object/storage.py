from functools import lru_cache
from typing import Any
import logging


class ObjectStorage:
    __slots__ = ("storage",)

    def __init__(self) -> None:
        self.storage = {}

    def put_record(self, key: str, record: Any) -> None:
        logging.info("Save data in object storage. Key: %s", key)
        self.storage.update({key: record})

    def get_record(self, key: str) -> Any | None:
        logging.info("Retrieve data from object storage. Key: %s", key)
        return self.storage.get(key)

    def record_exists(self, key: str) -> bool:
        logging.info("Check the record existence by key.")
        return True if self.storage.get(key) else False

    def delete_record(self, key: str) -> None:
        logging.info("Retrieve data from object storage. Key: %s", key)
        self.storage.pop(key, None)

    def update_record(self, key: str, record: Any) -> None:
        logging.info("Update data in object storage. Key: %s", key)
        self.storage.update({key: record})


object_storage: ObjectStorage | None = None


@lru_cache
def get_object_storage():
    return object_storage
