from functools import lru_cache

from telethon import TelegramClient


class ClientCheckHandler:
    __slots__ = ()

    def check_file_existence(self):
        pass

    async def check_connection(self):
        pass

    async def check_init_status(self):
        pass

    async def check(self, client: TelegramClient):
        self.check_file_existence()
        await self.check_connection()
        await self.check_init_status()


@lru_cache
def get_client_check_handler() -> ClientCheckHandler:
    return ClientCheckHandler()
