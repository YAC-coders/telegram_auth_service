import os

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
