import logging
from .interfaces import AbstractSecretReader

logger = logging.getLogger("core_creator.readers")

class EnvSecretReader(AbstractSecretReader):
    """Reads a secret directly from an environment variable."""
    def __init__(self, secret_data: str):
        self.secret_data = secret_data

    def read_secret(self) -> str:
        logger.info("Reading manually provided secret data.")
        return self.secret_data
