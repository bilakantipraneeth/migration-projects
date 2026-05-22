import sys
import logging
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound

logger = logging.getLogger("gcp.verify")

def verify_gcp_secret_exists(project_id: str, secret_id: str) -> str:
    """Checks if the Secret shell exists in GCP (Created by Platform Team)."""
    gcp_client = secretmanager.SecretManagerServiceClient()
    secret_path = gcp_client.secret_path(project_id, secret_id)
    
    logger.info(f"Checking if GCP Secret shell exists: {secret_path}")
    try:
        gcp_client.get_secret(request={"name": secret_path})
        logger.info("GCP Secret shell found.")
        return secret_path
    except NotFound:
        logger.error(f"CRITICAL: Secret shell '{secret_id}' does NOT exist in project '{project_id}'!")
        logger.error("The Platform Team must create the Terraform infrastructure for this secret before migration.")
        sys.exit(1)
