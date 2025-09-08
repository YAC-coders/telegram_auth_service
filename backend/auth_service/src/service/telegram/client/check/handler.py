from functools import lru_cache
import logging
import os

from telethon import TelegramClient

from core.settings import settings


class ClientCheckHandler:
    __slots__ = ()


    @staticmethod
    def remove_session_file(phone_number):
        path = os.path.join(settings.path.session_dir, f"{phone_number}.session")
        try:
            os.remove(path)
            logging.info(f"Deleted: {path}")
        except OSError as exception:
            logging.warning("Error deleting %s. Error: %s", path, str(exception))

    @staticmethod
    def check_file_existence(phone_number: str) -> bool:
        path = os.path.join(settings.path.session_dir, f"{phone_number}.session")
        return os.path.exists(path=path)

    @staticmethod
    async def check_connection(client: TelegramClient) -> bool:
        logging.info("Check %s account connection status.", client.session)
        try:
            logging.info("Connect to telegram servers...")
            await client.connect()
            return True
        except OSError:
            logging.warning("Fail to connect to telegram servers.")
            return False

    @staticmethod
    async def check_init_status(client: TelegramClient) -> bool:
        logging.info("Check %s account auth status.", client.session)
        if await client.is_user_authorized():
            logging.info("Account is authorized")
            await client.disconnect()
            return False
        return True


@lru_cache
def get_client_check_handler() -> ClientCheckHandler:
    return ClientCheckHandler()
