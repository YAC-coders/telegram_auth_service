import logging
import datetime

from fastapi import Depends
from telethon import errors

from db.redis.storage import RedisStorage, get_redis
from db.object.storage import ObjectStorage, get_object_storage
from service.crypt import CryptRepository, get_crypt_repo
from schema.auth.validate_code import ValidateCodeRequest, ValidateCodeResponse


class ValidateCodeService:
    __slots__ = ("_redis_storage", "_object_storage", "_crypt_repo")

    def __init__(
        self,
        redis_storage: RedisStorage,
        object_storage: ObjectStorage,
        crypt_repo: CryptRepository,
    ) -> None:
        self._redis_storage = redis_storage
        self._object_storage = object_storage
        self._crypt_repo = crypt_repo

    async def validate(
        self, validate_code_request: ValidateCodeRequest
    ) -> ValidateCodeResponse:
        phone_number = self._crypt_repo.decrypt(value=validate_code_request.session)

        client_info = self._object_storage.get_record(key=phone_number)
        if client_info:
            if client_info.get("step") == "validate_code":
                registration_timedelta = (
                    datetime.datetime.now() - client_info.get("timestamp")
                ).seconds
                if registration_timedelta < 300:
                    client = client_info.get("client")

                    try:
                        await client.sign_in(code=validate_code_request.code)
                        return ValidateCodeResponse(
                            session=validate_code_request.session, step="final"
                        )
                    except errors.SessionPasswordNeededError:
                        logging.info("Fail to login via code. Need cloud password.")
                        return ValidateCodeResponse(
                            session=validate_code_request.session, step="validate_password"
                        )

                logging.info(
                    "Registration time was expired for phone: %s",
                    phone_number,
                )
                self._object_storage.delete_record(key=phone_number)
                return ValidateCodeResponse(
                    session=validate_code_request.session, step="send_code"
                )

            else:
                return ValidateCodeResponse(
                    session=validate_code_request.session, step=client_info.get("step")
                )

        logging.warning(
            "Telegram connection was corrupted or was expired. Account phone number: %s",
            phone_number,
        )
        return ValidateCodeResponse(
            session=validate_code_request.session, step="send_code"
        )


def get_validate_code_service(
    redis_storage: RedisStorage = Depends(get_redis),
    object_storage: ObjectStorage = Depends(get_object_storage),
    crypt_repo: CryptRepository = Depends(get_crypt_repo),
) -> ValidateCodeService:
    return ValidateCodeService(
        redis_storage=redis_storage,
        object_storage=object_storage,
        crypt_repo=crypt_repo,
    )
