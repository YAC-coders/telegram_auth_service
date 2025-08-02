from functools import lru_cache

from telethon import TelegramClient

from service.telegram.client.entity import Client
from service.telegram.client.provider import (
    SimpleStringClientProvider,
    ProxyStringClientProvider,
)


class ClientRepository:
    __slots__ = ("string",)

    def __init__(self) -> None:
        self.string = self.String()

    class String:
        __slots__ = ()

        def simple(self) -> TelegramClient:
            return Client(provider=SimpleStringClientProvider()).create()

        def proxy(self) -> TelegramClient:
            return Client(provider=ProxyStringClientProvider()).create()


@lru_cache
def get_client_repository() -> ClientRepository:
    return ClientRepository()
