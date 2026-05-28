from abc import ABC, abstractmethod

class AbstractSecretReader(ABC):
    @abstractmethod
    def read_secret(self) -> str:
        pass

class AbstractSecretWriter(ABC):
    @abstractmethod
    def write_secret(self, payload: str) -> None:
        pass
