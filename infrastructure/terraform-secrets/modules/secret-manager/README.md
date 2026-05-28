# Reusable Secret Manager Module

This folder is a **Terraform Module**. A module is essentially a custom, reusable building block. Instead of writing the same resource block in every environment (Dev, Staging, Prod), you write it **once** here.

## How it works
This module takes two variables (`project_id` and `secrets`) and loops over them using the `for_each` meta-argument to automatically provision as many `google_secret_manager_secret` shells as you need.

## Why do we do this?
By keeping the core logic in `modules/secret-manager` and calling it from `envs/dev` or `envs/prod`:
1. **DRY (Don't Repeat Yourself):** You don't duplicate code. If you want to change how a secret is configured globally, you only change it here.
2. **Safety:** Dev and Prod share the exact same underlying logic, guaranteeing that what you test in Dev is exactly what gets deployed in Prod.
