# Development Environment

This folder is the "caller" for the Development environment. It does not define resources directly. Instead, it calls the `secret-manager` module.

## How to use this folder

1. **Configure your variables:** Edit the `dev.auto.tfvars` file to list exactly what secrets you want created in your Dev GCP project. You can also specify the `project_id` there.
2. **Initialize Terraform:**
   ```bash
   terraform init
   ```
   *This command reaches out to `../../modules/secret-manager` and downloads the module locally.*
3. **Plan and Apply:**
   ```bash
   terraform plan
   terraform apply
   ```

Because this is isolated in `envs/dev`, running `terraform apply` here will **only** affect your Dev project and Dev secrets!
