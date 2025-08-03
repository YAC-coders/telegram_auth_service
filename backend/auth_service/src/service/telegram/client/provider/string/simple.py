from telethon import TelegramClient
from telethon.sessions import StringSession

from service.telegram.client.provider.base import BaseClientProvider


class SimpleStringClientProvider(BaseClientProvider):
    def create(self) -> TelegramClient:
        return TelegramClient(
            session=StringSession(), api_id=self._api_id, api_hash=self._api_hash
        )
