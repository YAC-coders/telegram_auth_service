from functools import lru_cache
from typing import Any
import logging


class ObjectStorage:
    __slots__ = ("storage",)

    def __init__(self) -> None:
        self.storage = {}

    def put_record(self, key: str, record: Any) -> None:
        logging.info("Try to save data in object storage. Key: %s", key)
        self.storage.update({key: record})
        return None

    def get_record(self, key: str) -> Any | None:
        logging.info("Try to retrieve data from object storage. Key: %s", key)
        return self.storage.get(key)


object_storage: ObjectStorage | None = None


@lru_cache
def get_object_storage():
    return object_storage
