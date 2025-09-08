import logging
import datetime

from telethon import TelegramClient

from core.settings import settings
from exception.telegram import AlreadyLoggedIn
from service.auth.send_code.connection_processing.provider.interface import (
    ProviderInterface,
)
from service.telegram.client.create import ClientRepository, get_client_repository
from service.crypt import CryptRepository, get_crypt_repo


class NewConnectionProcessionProvider(ProviderInterface):
    STEP = "validate_code"

    __slots__ = ("phone_number", "_client_repo", "_crypt_repo")

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

        self._client_repo: ClientRepository = get_client_repository()
        self._crypt_repo: CryptRepository = get_crypt_repo()

    def _create_client(self, phone_number: str) -> TelegramClient:
        if settings.telegram.use_proxy:
            logging.info("Create telegram client with proxy.")
            return self._client_repo.sqlite.proxy(phone_number=phone_number)
        logging.info("Create simple telegram client.")
        return self._client_repo.sqlite.simple(phone_number=phone_number)

    async def _connect_to_telegram(self, client: TelegramClient) -> None:
        try:
            logging.info("Connect to telegram servers...")
            await client.connect()
        except OSError:
            logging.warning("Fail to connect to telegram servers.")

    async def _check_session_auth_status(self, client: TelegramClient) -> None:
        logging.info("Check account auth status.")
        if await client.is_user_authorized():
            await client.disconnect()
            raise AlreadyLoggedIn(
                f"Account with phone number: {self.phone_number} already logged in."
            )

    async def _send_code(self, client: TelegramClient):
        logging.info("Sending code to phone number: %s", self.phone_number)
        await client.send_code_request(self.phone_number)

    def encrypt_phone_number(self):
        return self._crypt_repo.encrypt(value=self.phone_number)

    async def process(self):
        """Process new authentication session."""

        client = self._create_client(phone_number=self.phone_number)

        await self._connect_to_telegram(client=client)
        await self._check_session_auth_status(client=client)
        await self._send_code(client=client)

        return {
            "client": client,
            "encrypted_phone_number": self.encrypt_phone_number(),
            "step": self.STEP,
            "timestamp": datetime.datetime.now(),
        }
