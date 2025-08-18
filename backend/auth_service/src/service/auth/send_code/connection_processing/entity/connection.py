from typing import Any


from service.auth.send_code.connection_processing.provider.interface import (
    ProviderInterface,
)


class Connection:
    def __init__(self, provider: ProviderInterface) -> None:
        self._provider = provider

    async def process(self) -> dict[str, Any] | None:
        return await self._provider.process()
