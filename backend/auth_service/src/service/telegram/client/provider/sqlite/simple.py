from telethon import TelegramClient

from service.telegram.client.provider.sqlite.base import BaseSQLiteClientProvider


class SimpleSQLiteClientProvider(BaseSQLiteClientProvider):
    def create(self) -> TelegramClient:
        return TelegramClient(
            session=self._create_path(file=self.phone_number),
            api_id=self._api_id,
            api_hash=self._api_hash,
        )
