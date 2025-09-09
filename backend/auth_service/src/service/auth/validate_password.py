import datetime
import logging
from typing import Any

from fastapi import Depends
from telethon import TelegramClient

from db.object.storage import ObjectStorage, get_object_storage
from schema.auth import ValidatePasswordRequest, ValidatePasswordResponse, Step
from service.crypt import CryptRepository, get_crypt_repo
from exception.telegram import PasswordExpired


class ValidatePasswordService:
    STEP = str(Step.validate_password)
    __slots__ = ("_object_storage", "_crypt_repo")

    def __init__(
        self,
        object_storage: ObjectStorage,
        crypt_repo: CryptRepository,
    ) -> None:
        self._object_storage = object_storage
        self._crypt_repo = crypt_repo

    def _get_client_info(self, phone_number: str):
        """Retrieve client info from storage."""
        return self._object_storage.get_record(key=phone_number)

    def _is_validation_expired(self, timestamp: datetime.datetime) -> bool:
        """Check if validation period has expired."""
        return datetime.datetime.now() - timestamp > datetime.timedelta(minutes=5)

    async def _handle_successful_validation(
        self, client: TelegramClient, validate_password_request: ValidatePasswordRequest, phone_number: str, client_info: dict[str, Any]
    ) -> ValidatePasswordResponse:
        """Handle successful code validation."""
        try:
            await client.sign_in(password=validate_password_request.password)
            self._object_storage.delete_record(key=phone_number)
            return ValidatePasswordResponse(
                session=validate_password_request.session, step=str(Step.final)
            )
        except Exception as exception:
            logging.warning("Something went wrong when sign in via password. Error %s", str(exception))
            raise

    async def validate(self, validate_password_request: ValidatePasswordRequest) -> ValidatePasswordResponse:
        phone_number = self._crypt_repo.decrypt(value=validate_password_request.session)
        client_info = self._get_client_info(phone_number=phone_number)

        if not client_info:
            logging.warning(
                "Telegram connection was corrupted or was expired. Account phone number: %s",
                phone_number,
            )
            return ValidatePasswordResponse(
                session=validate_password_request.session, step=str(Step.send_code)
            )

        current_step = client_info.get("step")
        if current_step != self.STEP:
            return ValidatePasswordResponse(
                session=validate_password_request.session, step=current_step
            )

        if self._is_validation_expired(client_info.get("timestamp")):
            logging.warning(
                "Registration time was expired for phone: %s",
                phone_number,
            )
            self._object_storage.delete_record(key=phone_number)
            raise PasswordExpired("Registration time was expired for phone: %s")

        return await self._handle_successful_validation(
            client=client_info.get("client"),
            phone_number=phone_number,
            client_info=client_info,
            validate_password_request=validate_password_request,
        )



def get_validate_password_service(
    object_storage: ObjectStorage = Depends(get_object_storage),
    crypt_repo: CryptRepository = Depends(get_crypt_repo),
) -> ValidatePasswordService:
    return ValidatePasswordService(
        object_storage=object_storage,
        crypt_repo=crypt_repo,
    )
