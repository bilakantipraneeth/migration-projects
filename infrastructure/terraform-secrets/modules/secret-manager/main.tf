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

resource "google_secret_manager_secret" "secret_shells" {
  for_each  = var.secrets
  secret_id = each.key

  labels = each.value.labels

  replication {
    automatic = true
  }
}
