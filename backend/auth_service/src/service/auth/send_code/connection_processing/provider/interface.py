from abc import ABC, abstractmethod


class ProviderInterface(ABC):
    @abstractmethod
    async def process(self):
        raise NotImplementedError
