# Manual GCP Secret Creator

A robust Python package (`core_creator`) that allows you to manually build a secret shell and push a custom payload directly into Google Cloud Secret Manager without needing HashiCorp Vault.

## Testing & Usage Guide

To test or run this tool locally, you must have Python 3.10+ installed and be authenticated with Google Cloud on your machine.

### 1. Prerequisites
Open your terminal and authenticate to Google Cloud so the script can inherit your permissions:
```powershell
gcloud auth application-default login
```

### 2. Installation
Ensure you are in this `manual-creator` directory, then install the package:
```powershell
pip install .
```

### 3. Environment Variables
You must set the following environment variables before running the script:
```powershell
$env:GCP_PROJECT_ID="your-gcp-project-id"
$env:GCP_SECRET_ID="my-test-secret"
$env:SECRET_DATA="SuperSecretPassword123!"
```

### 4. Execution
Run the orchestrator:
```powershell
python run.py
```
> **Note:** If the secret shell (`GCP_SECRET_ID`) does not exist in your GCP project, this tool will automatically create it for you before injecting the payload.
