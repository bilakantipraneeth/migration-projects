# GCP Secrets Migration Architecture

This repository contains enterprise-grade tools to manage the migration and creation of Google Cloud Platform (GCP) Secret Manager secrets from HashiCorp Vault.

## Architecture Structure

- **`infrastructure/terraform-secrets`**: Contains the Terraform configuration necessary to build the infrastructure (secret shells) in GCP.
- **`tools/vault-migrator`**: A robust Python package (`core_migrator`) that hooks into Vault, pulls secrets, and safely injects them into GCP.
- **`tools/manual-creator`**: A Python package (`core_creator`) which allows you to manually build a secret shell and push a custom payload directly into GCP without needing Vault.

---

## Testing Guide

Follow these step-by-step instructions to test both the local python scripts and the remote GitHub Actions pipelines.

### Part 1: Testing Locally

To test locally, you must have Python 3.10+ installed and be authenticated with Google Cloud on your machine.

#### 1. Prerequisites
- **Google Cloud Auth**: Open your terminal and run `gcloud auth application-default login`. This will open a browser to log you in. The Python scripts will automatically use these credentials!
- **Vault Auth (For Migrator only)**: Make sure you have your Vault Address and Token ready.

#### 2. Testing `manual-creator` locally
This tool pushes raw data straight to GCP Secret Manager.

1. **Navigate to the tool's directory:**
   ```powershell
   cd tools/manual-creator
   ```
2. **Install the package dependencies:**
   ```powershell
   pip install .
   ```
3. **Set the required Environment Variables:**
   ```powershell
   $env:GCP_PROJECT_ID="your-gcp-project-id"
   $env:GCP_SECRET_ID="my-test-secret"
   $env:SECRET_DATA="SuperSecretPassword123!"
   ```
4. **Run the script:**
   ```powershell
   python run.py
   ```

#### 3. Testing `vault-migrator` locally
This tool pulls from Vault and pushes to GCP.

1. **Navigate to the tool's directory:**
   ```powershell
   cd tools/vault-migrator
   ```
2. **Install the package dependencies:**
   ```powershell
   pip install .
   ```
3. **Set the required Environment Variables:**
   ```powershell
   $env:VAULT_ADDR="http://127.0.0.1:8200"
   $env:VAULT_TOKEN="your-vault-root-token"
   $env:VAULT_PATH="secret/data/my-app"
   $env:GCP_PROJECT_ID="your-gcp-project-id"
   $env:GCP_SECRET_ID="my-test-secret"
   ```
4. **Run the script:**
   ```powershell
   python run.py
   ```

---

### Part 2: Testing the GitHub Action Pipelines

The pipelines are set up using `workflow_dispatch`, meaning they do **not** run automatically on push. You trigger them manually from the GitHub UI when you actually want to migrate data.

**Important:** Before you run pipelines, you must add your Secrets to the GitHub Repository:
1. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.
2. Add `GCP_SA_KEY_JSON`: The JSON content of a GCP Service Account Key that has permissions to create/write to Secret Manager.
3. Add `VAULT_ADDR`: Your Vault URL.
4. Add `VAULT_TOKEN`: A valid Vault Token.

#### Triggering the Pipelines

1. Go to your GitHub repository page in your browser.
2. Click on the **Actions** tab at the top.
3. On the left sidebar, you will see two workflows listed:
   - **Manual GCP Secret Creation**
   - **Vault to GCP Migration**
4. Click on the workflow you want to test.
5. On the right side of the screen, you will see a gray button that says **Run workflow**. Click it.
6. A dropdown menu will appear asking for the required inputs (e.g., `GCP Project ID`, `Secret ID`, `Data Payload`). Fill in these text boxes.
7. Click the green **Run workflow** button.
8. Wait a few seconds, and you will see the pipeline job appear on your screen. Click on it to watch the live logs of the Python script executing!
