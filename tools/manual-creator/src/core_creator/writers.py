import sys
import logging
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound
from .interfaces import AbstractSecretWriter

logger = logging.getLogger("core_creator.writers")

class GcpSecretWriter(AbstractSecretWriter):
    """Writes a secret version to GCP Secret Manager, optionally creating it."""
    def __init__(self, project_id: str, secret_id: str, auto_create: bool = False):
        self.project_id = project_id
        self.secret_id = secret_id
        self.auto_create = auto_create
        self.client = secretmanager.SecretManagerServiceClient()

    def _ensure_secret_exists(self) -> str:
        parent = f"projects/{self.project_id}"
        secret_path = self.client.secret_path(self.project_id, self.secret_id)
        
        try:
            self.client.get_secret(request={"name": secret_path})
            logger.info(f"Secret shell '{self.secret_id}' found in GCP.")
            return secret_path
        except NotFound:
            if self.auto_create:
                logger.info(f"Secret shell '{self.secret_id}' not found. Creating it...")
                self.client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": self.secret_id,
                        "secret": {"replication": {"automatic": {}}},
                    }
                )
                logger.info("Secret shell created successfully.")
                return secret_path
            else:
                logger.error(f"Secret shell '{self.secret_id}' does not exist and auto_create is disabled.")
                sys.exit(1)

    def write_secret(self, payload: str) -> None:
        secret_path = self._ensure_secret_exists()
        
        logger.info(f"Pushing secret data version to {self.secret_id}...")
        payload_bytes = payload.encode("UTF-8")
        
        self.client.add_secret_version(
            request={
                "parent": secret_path,
                "payload": {"data": payload_bytes},
            }
        )
        logger.info("Manual creation successful. New version added.")
