from functools import lru_cache

from telethon import TelegramClient

from service.telegram.client.create.entity import Client
from service.telegram.client.create.provider import (
    SimpleStringClientProvider,
    ProxyStringClientProvider,
    SimpleSQLiteClientProvider,
    ProxySQLiteClientProvider,
)


class ClientRepository:
    __slots__ = ("string", "sqlite")

    def __init__(self) -> None:
        self.string = self.String()
        self.sqlite = self.SQLite()

    class String:
        __slots__ = ()

        def simple(self) -> TelegramClient:
            return Client(provider=SimpleStringClientProvider()).create()

        def proxy(self) -> TelegramClient:
            return Client(provider=ProxyStringClientProvider()).create()

    class SQLite:
        __slots__ = ()

        def simple(self, phone_number: str) -> TelegramClient:
            return Client(
                provider=SimpleSQLiteClientProvider(phone_number=phone_number)
            ).create()

        def proxy(self, phone_number: str) -> TelegramClient:
            return Client(
                provider=ProxySQLiteClientProvider(phone_number=phone_number)
            ).create()


@lru_cache
def get_client_repository() -> ClientRepository:
    return ClientRepository()
