import sys
import logging
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound
from .interfaces import AbstractSecretWriter

logger = logging.getLogger("core_migrator.writers")

class GcpSecretWriter(AbstractSecretWriter):
    """Writes a secret version to GCP Secret Manager."""
    def __init__(self, project_id: str, secret_id: str, enforce_exists: bool = True):
        self.project_id = project_id
        self.secret_id = secret_id
        self.enforce_exists = enforce_exists
        self.client = secretmanager.SecretManagerServiceClient()

    def _verify_secret_exists(self) -> str:
        secret_path = self.client.secret_path(self.project_id, self.secret_id)
        try:
            self.client.get_secret(request={"name": secret_path})
            logger.info(f"Verified: Secret shell '{self.secret_id}' exists in GCP.")
            return secret_path
        except NotFound:
            if self.enforce_exists:
                logger.error(f"CRITICAL: Secret shell '{self.secret_id}' does NOT exist in GCP.")
                logger.error("The Terraform pipeline must create the secret infrastructure before data migration.")
                sys.exit(1)
            else:
                return secret_path

    def write_secret(self, payload: str) -> None:
        secret_path = self._verify_secret_exists()
        
        logger.info(f"Pushing secret to GCP Secret Manager: {self.secret_id}")
        payload_bytes = payload.encode("UTF-8")
        
        self.client.add_secret_version(
            request={
                "parent": secret_path,
                "payload": {"data": payload_bytes},
            }
        )
        logger.info("New version successfully added to GCP Secret Manager.")
