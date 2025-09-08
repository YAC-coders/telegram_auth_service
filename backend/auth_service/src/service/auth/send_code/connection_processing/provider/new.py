import logging
import datetime

from telethon import TelegramClient

from service.auth.send_code.connection_processing.provider.interface import (
    ProviderInterface,
)
from service.crypt import CryptRepository, get_crypt_repo
from service.telegram.client import ClientCreateContext, get_client_create_context


class NewConnectionProcessionProvider(ProviderInterface):
    STEP = "validate_code"

    __slots__ = ("phone_number", "_client_repo", "_crypt_repo")

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

        self._client_context: ClientCreateContext = get_client_create_context()
        self._crypt_repo: CryptRepository = get_crypt_repo()

    async def _connect_to_telegram(self, client: TelegramClient) -> None:
        try:
            logging.info("Connect to telegram servers...")
            await client.connect()
        except OSError:
            logging.warning("Fail to connect to telegram servers.")

    async def _send_code(self, client: TelegramClient):
        logging.info("Sending code to phone number: %s", self.phone_number)
        await client.send_code_request(self.phone_number)

    def encrypt_phone_number(self):
        return self._crypt_repo.encrypt(value=self.phone_number)

    async def process(self):
        """Process new authentication session."""

        client = await self._client_context.create(phone_number=self.phone_number)

        await self._connect_to_telegram(client=client)
        await self._send_code(client=client)

        return {
            "client": client,
            "encrypted_phone_number": self.encrypt_phone_number(),
            "step": self.STEP,
            "timestamp": datetime.datetime.now(),
        }
