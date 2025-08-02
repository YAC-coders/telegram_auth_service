from typing import Protocol


class ProviderProtocol(Protocol):
    def create(self): ...
