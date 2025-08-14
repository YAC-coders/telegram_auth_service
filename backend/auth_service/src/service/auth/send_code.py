import logging
import datetime

from fastapi import Depends
from telethon import TelegramClient

from core.settings import settings
from db.object.storage import ObjectStorage, get_object_storage
from schema.auth import SendCodeRequest, SendCodeResponse
from service.telegram.client import ClientRepository, get_client_repository
from service.crypt import CryptRepository, get_crypt_repo
from exception.telegram import AlreadyLoggedIn


class SendCodeService:
    __slots__ = ("_client_repo", "_object_storage", "_crypt_repo")

    def __init__(
        self,
        client_repo: ClientRepository,
        object_storage: ObjectStorage,
        crypt_repo: CryptRepository,
    ) -> None:
        self._client_repo = client_repo
        self._object_storage = object_storage
        self._crypt_repo = crypt_repo

    def _create_client(self, phone_number: str) -> TelegramClient:
        if settings.telegram.use_proxy:
            logging.info("Create telegram client with proxy.")
            return self._client_repo.sqlite.proxy(phone_number=phone_number)
        logging.info("Create simple telegram client.")
        return self._client_repo.sqlite.simple(phone_number=phone_number)

    async def _handle_new_session(self, phone_number: str) -> SendCodeResponse:
        """Handle new authentication session."""
        client = self._create_client(phone_number=phone_number)

        await client.connect()

        if await client.is_user_authorized():
            raise AlreadyLoggedIn(
                f"Account with phone number: {phone_number} already logged in."
            )

        logging.info("Sending code to phone number: %s", phone_number)
        await client.send_code_request(phone_number)

        encrypted_phone = self._crypt_repo.encrypt(phone_number)

        self._object_storage.put_record(
            key=phone_number,
            record={
                "client": client,
                "encrypted_phone_number": encrypted_phone,
                "step": "validate_code",
                "timestamp": datetime.datetime.now(),
            },
        )

        return SendCodeResponse(session=encrypted_phone, step="validate_code")

    def _handle_existing_session(self, phone_number: str) -> SendCodeResponse:
        """Retrieve existing session data."""
        client_info = self._object_storage.get_record(key=phone_number)

        logging.info("Retrieved existing session for phone: %s", phone_number)

        return SendCodeResponse(
            session=client_info["encrypted_phone_number"], step=client_info["step"]
        )

    async def send_code(self, send_code_request: SendCodeRequest) -> SendCodeResponse:
        """Main service method to handle sending verification codes."""
        connection = self._object_storage.get_record(send_code_request.phone_number)

        if connection:
            logging.info(
                "Existing session found for phone: %s", send_code_request.phone_number
            )
            registration_timedelta = (
                datetime.datetime.now() - connection.get("timestamp")
            ).seconds
            if registration_timedelta < 300:
                return self._handle_existing_session(send_code_request.phone_number)

            logging.info(
                "Registration time was expired for phone: %s",
                send_code_request.phone_number,
            )
            self._object_storage.delete_record(key=send_code_request.phone_number)

        logging.info("New session for phone: %s", send_code_request.phone_number)
        return await self._handle_new_session(send_code_request.phone_number)


def get_send_code_service(
    client_repo: ClientRepository = Depends(get_client_repository),
    object_storage: ObjectStorage = Depends(get_object_storage),
    crypt_repo: CryptRepository = Depends(get_crypt_repo),
) -> SendCodeService:
    return SendCodeService(
        client_repo=client_repo,
        object_storage=object_storage,
        crypt_repo=crypt_repo,
    )
