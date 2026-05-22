import os
import sys
import logging
import hvac

logger = logging.getLogger("vault.connect")

def initialize_vault_client() -> hvac.Client:
    """Initializes and authenticates the HashiCorp Vault client."""
    vault_addr = os.environ.get("VAULT_ADDR", "https://vault.internal:8200")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_token:
        logger.error("VAULT_TOKEN environment variable is missing!")
        sys.exit(1)

    logger.info(f"Connecting to Vault at {vault_addr}...")
    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        logger.error("Failed to authenticate to Vault. Check your VAULT_TOKEN.")
        sys.exit(1)
        
    logger.info("Successfully authenticated to HashiCorp Vault.")
    return client
