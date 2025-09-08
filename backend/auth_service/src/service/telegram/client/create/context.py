from functools import lru_cache
import logging

from fastapi import Depends
from telethon import TelegramClient

from core.settings import settings
from telegram.client.create.repository import ClientRepository, get_client_repository
from telegram.client.check import ClientCheckHandler, get_client_check_handler


class ClientCreateContext:
    __slots__ = ("_client_repo", "_client_check_handler")

    def __init__(
        self, client_repo: ClientRepository, client_check_handler: ClientCheckHandler
    ) -> None:
        self._client_repo = client_repo
        self._client_check_handler = client_check_handler

    def _create_client_instance(self, phone_number: str):
        if settings.telegram.use_proxy:
            logging.info("Create telegram client with proxy.")
            return self._client_repo.sqlite.proxy(phone_number=phone_number)
        logging.info("Create simple telegram client.")
        return self._client_repo.sqlite.simple(phone_number=phone_number)

    async def _check_client_instance(self, client: TelegramClient):
        return await self._client_check_handler.check(client=client)

    async def create(self, phone_number: str) -> TelegramClient | None:
        client = self._create_client_instance(phone_number=phone_number)
        check_result = await self._check_client_instance(client=client)
        if not check_result:
            return None
        return client


@lru_cache
def get_client_create_context(
    client_repo: ClientRepository = Depends(get_client_repository),
    client_check_handler: ClientCheckHandler = Depends(get_client_check_handler),
) -> ClientCreateContext:
    return ClientCreateContext(
        client_repo=client_repo, client_check_handler=client_check_handler
    )
