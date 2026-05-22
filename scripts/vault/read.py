import sys
import logging
import hvac

logger = logging.getLogger("vault.read")

def extract_secret_from_vault(vault_client: hvac.Client, vault_path: str, secret_key: str = "password") -> str:
    """Reads the static secret payload from Vault KV store."""
    logger.info(f"Extracting secret payload from Vault path: {vault_path}")
    try:
        # Assuming Vault KV v2
        response = vault_client.secrets.kv.v2.read_secret_version(path=vault_path)
        secret_payload = response['data']['data'].get(secret_key)
        
        if not secret_payload:
            logger.error(f"Key '{secret_key}' not found in Vault path '{vault_path}'.")
            sys.exit(1)
            
        logger.info("Successfully extracted payload from Vault.")
        return secret_payload
    except Exception as e:
        logger.error(f"Failed to read from Vault: {e}")
        sys.exit(1)
