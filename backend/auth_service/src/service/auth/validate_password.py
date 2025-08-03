import logging

from fastapi import Depends

from db.redis.storage import RedisStorage, get_redis
from db.object.storage import ObjectStorage, get_object_storage
from schema.auth import ValidatePasswordRequest, ValidatePasswordResponse
from service.crypt import CryptRepository, get_crypt_repo


class ValidatePasswordService:
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

    async def validate(self, validate_password_request: ValidatePasswordRequest):
        phone_number = self._crypt_repo.decrypt(value=validate_password_request.session)

        client_id = await self._redis_storage.get_record(key=phone_number)
        if client_id:
            client = self._object_storage.get_record(key=client_id.decode("utf-8"))
            if client:
                await client.sign_in(password=validate_password_request.password)
                return ValidatePasswordResponse(
                    session=validate_password_request.session
                )
        else:
            logging.warning(
                "Telegram auth time was expired. Account phone number: %s", phone_number
            )


def get_validate_password_service(
    redis_storage: RedisStorage = Depends(get_redis),
    object_storage: ObjectStorage = Depends(get_object_storage),
    crypt_repo: CryptRepository = Depends(get_crypt_repo),
) -> ValidatePasswordService:
    return ValidatePasswordService(
        redis_storage=redis_storage,
        object_storage=object_storage,
        crypt_repo=crypt_repo,
    )
