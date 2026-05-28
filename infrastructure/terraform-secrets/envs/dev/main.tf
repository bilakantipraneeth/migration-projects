terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
}

module "secret_manager" {
  # This points to the reusable core module we built
  source     = "../../modules/secret-manager"
  
  project_id = var.project_id
  secrets    = var.secrets
}
