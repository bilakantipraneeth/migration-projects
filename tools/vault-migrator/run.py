import sys
import logging
from core_migrator.config import ConfigManager
from core_migrator.readers import VaultSecretReader
from core_migrator.writers import GcpSecretWriter
from core_migrator.migrator import SecretMigrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("vault_migrate")

if __name__ == "__main__":
    logger.info("Starting Vault to GCP Secret Migration...")
    
    config = ConfigManager()
    config.validate()
    
    reader = VaultSecretReader(
        addr=config.vault_addr,
        token=config.vault_token,
        path=config.vault_path,
        key=config.vault_key
    )
    
    writer = GcpSecretWriter(
        project_id=config.gcp_project_id,
        secret_id=config.gcp_secret_id,
        enforce_exists=True 
    )
    
    migrator = SecretMigrator(reader=reader, writer=writer)
    
    try:
        migrator.execute()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)
