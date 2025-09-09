import logging
import datetime
from typing import Any

from fastapi import Depends
from telethon import TelegramClient
from telethon import errors

from db.object.storage import ObjectStorage, get_object_storage
from service.crypt import CryptRepository, get_crypt_repo
from schema.auth import ValidateCodeRequest, ValidateCodeResponse, Step
from exception.telegram import CodeExpired


class ValidateCodeService:
    STEP = str(Step.validate_code)
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
        self, client: TelegramClient, validate_code_request: ValidateCodeRequest, phone_number: str, client_info: dict[str, Any]
    ) -> ValidateCodeResponse:
        """Handle successful code validation."""
        try:
            await client.sign_in(code=validate_code_request.code)
            self._object_storage.delete_record(key=phone_number)
            return ValidateCodeResponse(
                session=validate_code_request.session, step=str(Step.final)
            )
        except errors.SessionPasswordNeededError:
            logging.info("Fail to login via code. Need cloud password.")
            self._object_storage.update_record(key=phone_number, record={
                "client": client,
                "encrypted_phone_number": client_info.get("encrypted_phone_number"),
                "step": str(Step.validate_password),
                "timestamp": datetime.datetime.now(),
            })
            return ValidateCodeResponse(
                session=validate_code_request.session, step=str(Step.validate_password)
            )

    async def validate(
        self, validate_code_request: ValidateCodeRequest
    ) -> ValidateCodeResponse:
        phone_number = self._crypt_repo.decrypt(value=validate_code_request.session)
        client_info = self._get_client_info(phone_number=phone_number)

        if not client_info:
            logging.warning(
                "Telegram connection was corrupted or was expired. Account phone number: %s",
                phone_number,
            )
            return ValidateCodeResponse(
                session=validate_code_request.session, step=str(Step.send_code)
            )

        current_step = client_info.get("step")
        if current_step != self.STEP:
            return ValidateCodeResponse(
                session=validate_code_request.session, step=current_step
            )

        if self._is_validation_expired(client_info.get("timestamp")):
            logging.warning(
                "Registration time was expired for phone: %s",
                phone_number,
            )
            self._object_storage.delete_record(key=phone_number)
            raise CodeExpired("Registration time was expired for phone: %s")

        return await self._handle_successful_validation(
            client=client_info.get("client"),
            phone_number=phone_number,
            client_info=client_info,
            validate_code_request=validate_code_request,
        )


def get_validate_code_service(
    object_storage: ObjectStorage = Depends(get_object_storage),
    crypt_repo: CryptRepository = Depends(get_crypt_repo),
) -> ValidateCodeService:
    return ValidateCodeService(
        object_storage=object_storage,
        crypt_repo=crypt_repo,
    )
