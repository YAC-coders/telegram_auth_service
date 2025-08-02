from functools import lru_cache
from cryptography.fernet import Fernet

from core.settings import settings


class CryptRepository:
    __slots__ = ("_fernet",)

    def __init__(self) -> None:
        self._fernet = Fernet(key=settings.crypt.key)

    def encrypt(self, value: str) -> str:
        return (self._fernet.encrypt(value.encode())).decode()

    def decrypt(self, value: str) -> str:
        return self._fernet.decrypt(value).decode()


@lru_cache
def get_crypt_repo() -> CryptRepository:
    return CryptRepository()
