import logging
from uuid import uuid4

from fastapi import Depends
from telethon import TelegramClient

from core.settings import settings
from db.redis.storage import RedisStorage, get_redis
from db.object.storage import ObjectStorage, get_object_storage
from schema.auth import SendCodeRequest, SendCodeResponse
from service.telegram.client import ClientRepository, get_client_repository
from service.crypt import CryptRepository, get_crypt_repo


class SendCodeService:
    __slots__ = ("_client_factory", "_redis_storage", "_object_storage", "_crypt_repo")

    def __init__(
        self,
        client_repo: ClientRepository,
        redis_storage: RedisStorage,
        object_storage: ObjectStorage,
        crypt_repo: CryptRepository,
    ) -> None:
        self._client_factory = client_repo
        self._redis_storage = redis_storage
        self._object_storage = object_storage
        self._crypt_repo = crypt_repo

    def _create_client(self):
        if settings.telegram.use_proxy:
            logging.info("Create telegram client with proxy.")
            return self._client_factory.string.proxy()
        logging.info("Create simple telegram client.")
        return self._client_factory.string.simple()

    async def _store_data_in_redis(self, phone_number: str, client_id: str) -> None:
        logging.info(
            "Store the client info in redis. Account phone number: %s",
            phone_number,
        )
        await self._redis_storage.put_record(
            record=client_id,
            key=phone_number,
            expires_in=5 * 60,
        )

    def _store_client_on_object(self, client_id: str, client: TelegramClient):
        logging.info(
            "Store the client object. Client id: %s",
            client_id,
        )
        self._object_storage.put_record(key=client_id, record=client)

    async def send_code(self, send_code_request: SendCodeRequest):
        client = self._create_client()

        await client.connect()

        if not await client.is_user_authorized():
            logging.info(
                "Try to send code to the phone number %s",
                send_code_request.phone_number,
            )
            await client.send_code_request(send_code_request.phone_number)

            client_id = str(uuid4())
            encrypted_phone_number = self._crypt_repo.encrypt(
                value=send_code_request.phone_number
            )

            await self._store_data_in_redis(
                phone_number=send_code_request.phone_number, client_id=client_id
            )

            self._store_client_on_object(client_id=client_id, client=client)

            return SendCodeResponse(session=encrypted_phone_number)


def get_send_code_service(
    client_repo: ClientRepository = Depends(get_client_repository),
    redis_storage: RedisStorage = Depends(get_redis),
    object_storage: ObjectStorage = Depends(get_object_storage),
    crypt_repo: CryptRepository = Depends(get_crypt_repo),
) -> SendCodeService:
    return SendCodeService(
        client_repo=client_repo,
        redis_storage=redis_storage,
        object_storage=object_storage,
        crypt_repo=crypt_repo,
    )
