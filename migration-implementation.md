# Vault to GCP Secret Manager: Migration Implementation Guide

This document outlines the standard operating procedure (SOP) for migrating **Secrets** from HashiCorp Vault to the Centralized GCP Secrets Architecture.

To ensure strict security and proper division of labor, we use a **Split-Responsibility Model** between the Platform Team and our Migration/DevOps Team.

---

## 1. Static Keys vs Dynamic Keys Explained

Before migrating, it's critical to understand the difference between Static and Dynamic keys in Vault:

### Static Keys
**What are they?** Fixed strings (e.g., API keys, SSL certificates, or static passwords) that are manually generated and rarely change. They are stored in Vault's KV (Key-Value) store.
**Migration Strategy**: We simply read the static payload from Vault and push it to GCP Secret Manager.

### Dynamic Keys
**What are they?** Short-lived credentials generated "on the fly" by Vault. For example, when an app asks Vault for database access, Vault logs into PostgreSQL, creates a temporary user (`app_user_123`) valid for 1 hour, and gives it to the app. 
**Migration Strategy**: GCP Secret Manager **does not natively generate dynamic keys** on the fly. To migrate this pattern, you must switch to the **Automated Rotation Pattern**. You store a permanent credential in GCP, and attach a Cloud Function that rotates the password automatically every 30 days. *Our current modular Python script only migrates Static Keys.*

---

## 2. Division of Responsibilities

### Platform Team Responsibility (Infrastructure)
The Platform Team is entirely responsible for provisioning the GCP infrastructure using **Terraform**. They handle:
- Creating the empty Secret Manager shells (e.g., `google_secret_manager_secret`).
- Provisioning Google Service Accounts (GSAs).

*Note: Terraform never handles or stores the actual secret payloads to prevent leaking secrets into state files.*

### Our Responsibility (Data Migration)
Our scope is strictly the **Data Migration**. Once the Platform Team confirms the infrastructure is ready, our automation will:
1. Securely authenticate to Vault using a Vault Token.
2. Securely authenticate to GCP using a Service Account JSON Key (`GOOGLE_APPLICATION_CREDENTIALS`).
3. Verify the secret shell exists. If it exists, read the data from Vault and push it as a new version.

---

## 3. Data Migration Pipeline setup

Our modular Python application (`scripts/main.py`) is executed via a GitHub Actions pipeline.

### Step 3.1: Environment Variable Setup in GitHub
To securely execute the Python script, the following secrets must be added to your GitHub Repository Secrets:

| GitHub Secret Name | Description | Where Pipeline Injects It |
|-------------------|-------------|---------------------------|
| `VAULT_TOKEN` | The authentication token to read from Vault. | Mapped to `os.environ['VAULT_TOKEN']` |
| `GCP_SA_KEY_JSON` | The raw JSON file of the GCP Service Account key. | Written to disk temporarily and mapped to `GOOGLE_APPLICATION_CREDENTIALS` |

### Step 3.2: GitHub Actions Workflow (`.github/workflows/migrate-secrets.yml`)
The pipeline triggers the modular app and securely handles dynamic inputs per migration run.

```yaml
name: Vault to GCP Secret Migration

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target Environment (prod or non-prod)'
        required: true
        default: 'non-prod'
        type: choice
        options:
          - non-prod
          - prod
      vault_path:
        description: 'Vault KV Path (e.g., apps/app-a/db-password)'
        required: true
        type: string
      gcp_secret_id:
        description: 'GCP Secret ID (e.g., app-db-password)'
        required: true
        type: string

jobs:
  migrate-secrets:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install hvac google-cloud-secret-manager

      - name: Authenticate to Google Cloud via Service Account Key
        id: auth
        uses: google-github-actions/auth@v2
        with:
          credentials_json: '${{ secrets.GCP_SA_KEY_JSON }}'

      - name: Run Modular Python Migration Script
        env:
          VAULT_TOKEN: ${{ secrets.VAULT_TOKEN }}
          VAULT_ADDR: 'https://vault.internal:8200'
          ENVIRONMENT: ${{ github.event.inputs.environment }}
          VAULT_PATH: ${{ github.event.inputs.vault_path }}
          GCP_SECRET_ID: ${{ github.event.inputs.gcp_secret_id }}
        run: |
          cd scripts
          python main.py
```

---

## 4. Execution Runbook & Error Handling

1. **Trigger Pipeline**: Run the pipeline from GitHub Actions, filling out the target environment, vault path, and GCP secret ID.
2. **Execution Logic (`scripts/main.py`)**:
   - **Environment Mapping (`config.py`)**: Validates if `ENVIRONMENT` is prod or non-prod to pick the right GCP project.
   - **Shell Verification (`gcp/verify.py`)**: Checks if the secret exists. **If it does not exist, the script throws a CRITICAL error and stops.**
   - **Versioning (`gcp/push.py`)**: If the secret exists, it pulls from Vault (`vault/read.py`) and calls `add_secret_version`. If a version already exists, GCP safely appends this as the *newest active version* without deleting history.
3. **Logs & Clean Up**: The script uses Python's standard `logging` library for perfectly clear outputs. The GCP Key file is wiped automatically when the GitHub Actions runner destroys itself.
