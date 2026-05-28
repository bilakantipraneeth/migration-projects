import logging
import hvac
from .interfaces import AbstractSecretReader

logger = logging.getLogger("core_migrator.readers")

class VaultSecretReader(AbstractSecretReader):
    """Reads a secret from HashiCorp Vault."""
    def __init__(self, addr: str, token: str, path: str, key: str):
        self.addr = addr.strip() if addr else addr
        self.token = token.strip() if token else token
        self.path = path.strip() if path else path
        self.key = key.strip() if key else key

    def read_secret(self) -> str:
        logger.info(f"Connecting to Vault at {self.addr}...")
        client = hvac.Client(url=self.addr, token=self.token)
        
        if not client.is_authenticated():
            raise Exception("Vault authentication failed.")
            
        logger.info(f"Reading secret from Vault path: {self.path}")
        
        parts = self.path.split('/', 1)
        if len(parts) == 2:
            mount_point = parts[0]
            secret_path = parts[1]
        else:
            mount_point = 'secret'
            secret_path = self.path
            
        response = client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=secret_path)
        secret_data = response['data']['data'].get(self.key)
        
        if not secret_data:
            raise Exception(f"Key '{self.key}' not found in Vault path '{self.path}'")
            
        return secret_data
