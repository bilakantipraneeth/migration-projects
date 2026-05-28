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

### 4. Environment Variables
You must set the following environment variables before running the script:
```powershell
$env:VAULT_ADDR="http://127.0.0.1:8200"
$env:VAULT_TOKEN="your-vault-root-token"
$env:VAULT_PATH="secret/my-app"
$env:GCP_PROJECT_ID="your-gcp-project-id"
$env:GCP_SECRET_ID="my-test-secret"
```
*(Optional: Set `$env:VAULT_KEY` if the specific key you want to pull from Vault is not named "password")*

### 5. Execution
Run the orchestrator:
```powershell
python run.py
```
> **Warning:** Unlike the manual-creator, this tool will **fail** if the secret shell does not already exist in GCP. The shells must be provisioned via Terraform beforehand.

## GitHub Actions CI/CD (Cloud VM)

You can run this migration tool entirely from the cloud using the pre-configured GitHub Actions pipelines! 
Because GitHub Actions cannot access your local `127.0.0.1` Docker container, we have built a Terraform module to temporarily spin up a public Vault VM in Google Cloud for testing.

### Step 1: Deploy the Vault VM
1. Go to your repository on GitHub > **Actions** tab.
2. Select **Deploy Vault VM** and click **Run workflow**.
3. When the workflow completes, open the logs and copy the `Vault Public URL` (e.g., `http://34.56.x.x:8200`).

### Step 2: Configure Secrets
Navigate to **Settings** > **Secrets and variables** > **Actions** and ensure these repository secrets exist:
- `GCP_SA_KEY_JSON`: Your Google Cloud JSON key (with Secret Manager Admin rights).
- `VAULT_ADDR`: Paste the URL from Step 1. **(CRITICAL: It must include the `http://` prefix, e.g., `http://34.56.x.x:8200`)**
- `VAULT_TOKEN`: `test-root-token`

### Step 3: Run the Migration Pipeline
1. Go back to the **Actions** tab.
2. Select **Vault to GCP Migration** and click **Run workflow**. 
3. Use the following test values:
   - **Vault Path**: `secret/my-app` *(The VM automatically injects the payload here)*
   - **Vault Key Name**: `password`
   - **GCP Project ID**: `praneeth1211-gcp-pilot`
   - **GCP Secret ID**: `ai-test-secret` *(Or any secret shell you have deployed)*
4. Click **Run workflow** and watch the logs as your data is securely migrated!
