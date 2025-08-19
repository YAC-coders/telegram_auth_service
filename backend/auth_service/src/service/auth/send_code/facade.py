import logging

from fastapi import Depends

from db.object.storage import ObjectStorage, get_object_storage
from schema.auth import SendCodeRequest, SendCodeResponse
from service.auth.send_code.connection_processing.entity import Connection
from service.auth.send_code.connection_processing.provider import (
    ExistsConnectionProcessionProvider,
    NewConnectionProcessionProvider,
)


class SendCodeService:
    __slots__ = ("_object_storage",)

    def __init__(
        self,
        object_storage: ObjectStorage,
    ) -> None:
        self._object_storage = object_storage

    async def _handle_new_connection(self, phone_number: str) -> SendCodeResponse:
        """Handle new authentication session."""
        logging.info("New session for phone: %s", phone_number)

        client_info = await Connection(
            provider=NewConnectionProcessionProvider(phone_number=phone_number)
        ).process()

        self._object_storage.put_record(
            key=phone_number,
            record=client_info,
        )

        return SendCodeResponse(
            session=client_info["encrypted_phone_number"], step=client_info["step"]
        )

    async def _handle_exists_connection(
        self, connection, phone_number: str
    ) -> SendCodeResponse:
        """Handle exists authentication session."""

        logging.info("Existing session found for phone: %s", phone_number)

        client_info = await Connection(
            provider=ExistsConnectionProcessionProvider(client_info=connection)
        ).process()
        if client_info:
            return SendCodeResponse(
                session=client_info["encrypted_phone_number"], step=client_info["step"]
            )

        logging.info(
            "Registration time was expired for phone: %s",
            phone_number,
        )
        self._object_storage.delete_record(key=phone_number)
        return await self._handle_new_connection(phone_number=phone_number)

    async def send_code(self, send_code_request: SendCodeRequest) -> SendCodeResponse:
        """Main service method to handle sending verification codes."""
        connection = self._object_storage.get_record(send_code_request.phone_number)
        if connection:
            return await self._handle_exists_connection(
                connection=connection, phone_number=send_code_request.phone_number
            )
        return await self._handle_new_connection(
            phone_number=send_code_request.phone_number
        )


def get_send_code_service(
    object_storage: ObjectStorage = Depends(get_object_storage),
) -> SendCodeService:
    return SendCodeService(
        object_storage=object_storage,
    )
