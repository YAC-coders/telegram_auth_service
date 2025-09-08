from functools import lru_cache
import logging

from telethon import TelegramClient

from exception.telegram import AlreadyLoggedIn


class ClientCheckHandler:
    __slots__ = ()

    def check_file_existence(self) -> bool:
        pass

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
            raise AlreadyLoggedIn(
                f"Account with phone number: {self.phone_number} already logged in."
            )
        return True


@lru_cache
def get_client_check_handler() -> ClientCheckHandler:
    return ClientCheckHandler()
