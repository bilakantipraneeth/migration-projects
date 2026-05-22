import sys
import logging
from google.cloud import secretmanager

logger = logging.getLogger("gcp.push")

def push_to_gcp_secret_manager(secret_path: str, payload: str):
    """Adds a new version to the GCP Secret Manager."""
    gcp_client = secretmanager.SecretManagerServiceClient()
    logger.info(f"Pushing payload to GCP Secret Manager: {secret_path}")
    
    payload_bytes = payload.encode("UTF-8")
    
    try:
        response = gcp_client.add_secret_version(
            request={
                "parent": secret_path,
                "payload": {"data": payload_bytes},
            }
        )
        version_id = response.name.split('/')[-1]
        logger.info(f"Successfully created new Secret Version: v{version_id}")
    except Exception as e:
        logger.error(f"Failed to push to GCP Secret Manager: {e}")
        sys.exit(1)
