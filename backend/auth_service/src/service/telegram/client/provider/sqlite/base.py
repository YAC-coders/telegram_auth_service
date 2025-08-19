import os
import logging

from core.settings import settings
from service.telegram.client.provider.base import BaseClientProvider


class BaseSQLiteClientProvider(BaseClientProvider):
    __slots__ = ("_api_id", "_api_hash", "phone_number")

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

        self._api_id: int = settings.telegram.api_id
        self._api_hash: str = settings.telegram.api_hash

    @staticmethod
    def _create_path(file: str) -> str:
        return os.path.join(settings.path.session_dir, file)

    @staticmethod
    def _check_session_existence(path: str) -> bool:
        return os.path.exists(path=path)

    def _clean_dir(self) -> None:
        path = os.path.join(settings.path.session_dir, f"{self.phone_number}.session")
        if self._check_session_existence(path=path):
            try:
                os.remove(path)
                logging.info(f"Deleted: {path}")
            except OSError as exception:
                logging.warning("Error deleting %s. Error: %s", path, str(exception))
