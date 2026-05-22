import os
import sys
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def get_gcp_project_id() -> str:
    """Determines the correct GCP project based on the environment."""
    PROJECT_MAP = {
        "prod": "prj-secrets-core",
        "non-prod": "prj-secrets-nonprod"
    }
    
    env = os.environ.get("ENVIRONMENT", "").lower()
    logger = logging.getLogger("config")
    
    if env not in PROJECT_MAP:
        logger.error(f"Invalid or missing ENVIRONMENT. Must be 'prod' or 'non-prod'. Found: '{env}'")
        sys.exit(1)
        
    project_id = PROJECT_MAP[env]
    logger.info(f"Environment detected: {env.upper()}. Using GCP Project: {project_id}")
    return project_id
