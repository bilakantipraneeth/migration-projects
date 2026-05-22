import os
import sys
import logging

# Configuration & Sub-package imports
from config import setup_logging, get_gcp_project_id
from vault.connect import initialize_vault_client
from vault.read import extract_secret_from_vault
from gcp.verify import verify_gcp_secret_exists
from gcp.push import push_to_gcp_secret_manager

def run_migration():
    setup_logging()
    logger = logging.getLogger("main")
    
    logger.info("Starting Vault to GCP Secret Migration Pipeline...")
    
    # Ensure GCP Service Account Key is provided via ENV
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        logger.error("GOOGLE_APPLICATION_CREDENTIALS env var is missing. Required for GCP authentication.")
        sys.exit(1)

    # Variables for this specific run
    vault_path = os.environ.get("VAULT_PATH", "apps/app-a/db-password")
    vault_key = os.environ.get("VAULT_KEY", "password")
    gcp_secret_id = os.environ.get("GCP_SECRET_ID", "app-db-password")
    
    # 1. Initialize Vault
    vault_client = initialize_vault_client()
    
    # 2. Determine Environment and Project
    project_id = get_gcp_project_id()
    
    # 3. Verify GCP Infrastructure exists
    gcp_secret_path = verify_gcp_secret_exists(project_id, gcp_secret_id)
    
    # 4. Extract data from Vault
    secret_payload = extract_secret_from_vault(vault_client, vault_path, vault_key)
    
    # 5. Inject as a new version in GCP
    push_to_gcp_secret_manager(gcp_secret_path, secret_payload)
    
    logger.info("Migration process completed successfully.")

if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        logging.error(f"Migration failed due to an unexpected error: {e}")
        sys.exit(1)
