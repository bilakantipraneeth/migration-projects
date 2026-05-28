import os
import sys
import logging

logger = logging.getLogger("core_creator.config")

class ConfigManager:
    """Responsible for loading and validating environment variables."""
    def __init__(self):
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID")
        self.gcp_secret_id = os.environ.get("GCP_SECRET_ID")
        self.secret_data = os.environ.get("SECRET_DATA")

    def validate(self):
        if not all([self.gcp_project_id, self.gcp_secret_id, self.secret_data]):
            logger.error("Missing required environment variables (GCP_PROJECT_ID, GCP_SECRET_ID, SECRET_DATA)")
            sys.exit(1)
