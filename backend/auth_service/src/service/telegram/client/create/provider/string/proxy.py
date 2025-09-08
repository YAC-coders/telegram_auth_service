from telethon import TelegramClient
from telethon.sessions import StringSession

from core.settings import settings
from service.telegram.client.create.provider.base import BaseClientProvider


class ProxyStringClientProvider(BaseClientProvider):
    def create(self) -> TelegramClient:
        return TelegramClient(
            session=StringSession(),
            api_id=self._api_id,
            api_hash=self._api_hash,
            proxy=(settings.proxy.scheme, settings.proxy.hostname, settings.proxy.port),
        )
