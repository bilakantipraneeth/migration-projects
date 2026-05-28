import sys
import logging
from core_creator.config import ConfigManager
from core_creator.readers import EnvSecretReader
from core_creator.writers import GcpSecretWriter
from core_creator.migrator import SecretMigrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("manual_create")

if __name__ == "__main__":
    logger.info("Starting Manual Secret Creation...")
    
    config = ConfigManager()
    config.validate()
    
    reader = EnvSecretReader(secret_data=config.secret_data)
    
    # auto_create is True because this is the manual tool that is allowed to create secrets.
    writer = GcpSecretWriter(
        project_id=config.gcp_project_id,
        secret_id=config.gcp_secret_id,
        auto_create=True
    )
    
    migrator = SecretMigrator(reader=reader, writer=writer)
    
    try:
        migrator.execute()
    except Exception as e:
        logger.error(f"Manual creation failed: {e}")
        sys.exit(1)
