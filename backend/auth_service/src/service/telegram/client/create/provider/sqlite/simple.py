from telethon import TelegramClient

from service.telegram.client.create.provider.sqlite.base import BaseSQLiteClientProvider


class SimpleSQLiteClientProvider(BaseSQLiteClientProvider):
    def create(self) -> TelegramClient:
        self._clean_dir()
        return TelegramClient(
            session=self._create_path(file=self.phone_number),
            api_id=self._api_id,
            api_hash=self._api_hash,
        )
