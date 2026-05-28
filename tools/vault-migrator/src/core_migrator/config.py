import os
import sys
import logging

logger = logging.getLogger("core_migrator.config")

class ConfigManager:
    """Responsible for loading and validating environment variables."""
    def __init__(self):
        self.vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
        self.vault_token = os.environ.get("VAULT_TOKEN")
        self.vault_path = os.environ.get("VAULT_PATH")
        self.vault_key = os.environ.get("VAULT_KEY", "password")
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID")
        self.gcp_secret_id = os.environ.get("GCP_SECRET_ID")

    def validate(self):
        if not all([self.vault_token, self.vault_path, self.gcp_project_id, self.gcp_secret_id]):
            logger.error("Missing required environment variables (VAULT_TOKEN, VAULT_PATH, GCP_PROJECT_ID, GCP_SECRET_ID)")
            sys.exit(1)
