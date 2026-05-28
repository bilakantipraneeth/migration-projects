# Production Environment

This folder is the "caller" for the Production environment. It relies on the identical code inside `modules/secret-manager` to ensure parity with Development.

## Important Note for Prod
Because this is Production, you should typically run this through a CI/CD pipeline rather than applying it from your local machine, and you should configure a Remote Backend (like a GCS bucket) to store your state file safely.

## How to use this folder

1. **Configure your variables:** Edit the `prod.auto.tfvars` file to list the exact secrets needed in Prod. 
2. **Initialize Terraform:**
   ```bash
   terraform init
   ```
3. **Plan and Apply:**
   ```bash
   terraform plan
   terraform apply
   ```

This will **only** touch your Prod project!
