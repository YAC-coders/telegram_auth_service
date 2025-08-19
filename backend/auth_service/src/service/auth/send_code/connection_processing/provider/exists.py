import datetime
from typing import Any


from service.auth.send_code.connection_processing.provider.interface import (
    ProviderInterface,
)


class ExistsConnectionProcessionProvider(ProviderInterface):
    __slots__ = ("client_info",)

    def __init__(self, client_info: dict[str, Any]) -> None:
        self.client_info = client_info

    async def process(self):
        """Process exists authentication session."""
        registration_timedelta = (
            datetime.datetime.now() - self.client_info.get("timestamp")
        ).seconds

        if registration_timedelta < 300:
            return self.client_info
        return None
