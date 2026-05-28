# Vault to GCP Migrator

A robust Python package (`core_migrator`) that connects to HashiCorp Vault, securely pulls secret payloads, and safely injects them into Google Cloud Secret Manager.

## Testing & Usage Guide

To test or run this tool locally, you must have Python 3.10+ installed and be authenticated with Google Cloud on your machine.

### 1. Prerequisites
- **Google Cloud:** Open your terminal and authenticate:
  ```powershell
  gcloud auth application-default login
  ```

### 2. Vault Docker Testing Environment (Recommended)
If you don't have a Vault server to test with, you can spin one up instantly using Docker!
1. Open PowerShell and navigate to the local testing environment:
   ```powershell
   cd local-env
   ```
2. Run the automated setup script. This spins up Vault and safely injects a test secret into it using Docker Exec:
   ```powershell
   .\setup-vault.ps1
   ```
3. Your local Vault is now running on `http://127.0.0.1:8200` with the token `test-root-token`.

### 3. Installation
Ensure you are in this `vault-migrator` directory, then install the package:
```powershell
pip install .
```

### 3. Environment Variables
You must set the following environment variables before running the script:
```powershell
$env:VAULT_ADDR="http://127.0.0.1:8200"
$env:VAULT_TOKEN="your-vault-root-token"
$env:VAULT_PATH="secret/data/my-app"
$env:GCP_PROJECT_ID="your-gcp-project-id"
$env:GCP_SECRET_ID="my-test-secret"
```
*(Optional: Set `$env:VAULT_KEY` if the specific key you want to pull from Vault is not named "password")*

### 4. Execution
Run the orchestrator:
```powershell
python run.py
```
> **Warning:** Unlike the manual-creator, this tool will **fail** if the secret shell does not already exist in GCP. The shells must be provisioned via Terraform beforehand.
