import logging
import hvac
from .interfaces import AbstractSecretReader

logger = logging.getLogger("core_migrator.readers")

class VaultSecretReader(AbstractSecretReader):
    """Reads a secret from HashiCorp Vault."""
    def __init__(self, addr: str, token: str, path: str, key: str):
        self.addr = addr
        self.token = token
        self.path = path
        self.key = key

    def read_secret(self) -> str:
        logger.info(f"Connecting to Vault at {self.addr}...")
        client = hvac.Client(url=self.addr, token=self.token)
        
        if not client.is_authenticated():
            raise Exception("Vault authentication failed.")
            
        logger.info(f"Reading secret from Vault path: {self.path}")
        response = client.secrets.kv.v2.read_secret_version(path=self.path)
        secret_data = response['data']['data'].get(self.key)
        
        if not secret_data:
            raise Exception(f"Key '{self.key}' not found in Vault path '{self.path}'")
            
        return secret_data
