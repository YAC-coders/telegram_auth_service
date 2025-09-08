from functools import lru_cache
import logging

from fastapi import Depends
from telethon import TelegramClient

from core.settings import settings
from exception.telegram import AlreadyLoggedIn
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

    async def create(self, phone_number: str) -> TelegramClient:
        client = self._create_client_instance(phone_number=phone_number)
        check_dir_result = self._client_check_handler.check_file_existence(
            phone_number=phone_number
        )
        if check_dir_result:
            check_connection_result = await self._client_check_handler.check_connection(
                client=client
            )
            if check_connection_result:
                check_init_result = await self._client_check_handler.check_init_status(
                    client=client
                )
                if check_init_result:
                    raise AlreadyLoggedIn(
                    f"Account with phone number: {phone_number} already logged in."
                )
                await self._client_check_handler.disconnect_from_telegram_server(client=client)
                return client

            self._client_check_handler.remove_session_file(
                phone_number=phone_number
            )
        return client


@lru_cache
def get_client_create_context(
    client_repo: ClientRepository = Depends(get_client_repository),
    client_check_handler: ClientCheckHandler = Depends(get_client_check_handler),
) -> ClientCreateContext:
    return ClientCreateContext(
        client_repo=client_repo, client_check_handler=client_check_handler
    )
