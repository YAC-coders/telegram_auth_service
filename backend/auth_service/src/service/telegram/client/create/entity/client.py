import logging

from telethon import TelegramClient

from service.telegram.client.provider import ProviderProtocol


class Client:
    def __init__(self, provider: ProviderProtocol) -> None:
        self._provider = provider

    def create(self) -> TelegramClient:
        logging.info(
            "Try to create the telegram client with provider: %s", str(self._provider)
        )
        return self._provider.create()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(provider={self._provider})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<provider={self._provider!r}>"
