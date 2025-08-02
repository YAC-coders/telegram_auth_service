from core.settings import settings


class BaseClientProvider:
    __slots__ = ("_api_id", "_api_hash")

    def __init__(self) -> None:
        self._api_id: int = settings.telegram.api_id
        self._api_hash: str = settings.telegram.api_hash

    def create(self):
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(api_id={self._api_id}, api_hash={self._api_hash})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<api_id={self._api_id!r}, api_hash={self._api_hash!r}>"
