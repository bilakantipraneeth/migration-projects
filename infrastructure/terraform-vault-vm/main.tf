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
  region  = var.region
}

# Firewall rule to allow Vault UI/API (8200) from anywhere
resource "google_compute_firewall" "vault_fw" {
  name    = "allow-vault-api"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8200", "22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["vault-server"]
}

# The Compute Engine VM
resource "google_compute_instance" "vault_vm" {
  name         = "vault-test-server"
  machine_type = "e2-micro"
  zone         = var.zone

  tags = ["vault-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 10
    }
  }

  network_interface {
    network = "default"
    # The access_config block gives the VM an ephemeral public IP
    access_config {
      // Ephemeral IP
    }
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    set -e
    
    # Update and install dependencies
    apt-get update -y
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

    # Install Docker
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io

    # Run HashiCorp Vault in dev mode on port 8200, exposed to all interfaces
    docker run -d --name vault-dev -p 8200:8200 --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=test-root-token' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' hashicorp/vault:latest

    # Wait for Vault to start
    sleep 10

    # Inject test payload
    docker exec -e VAULT_TOKEN="test-root-token" -e VAULT_ADDR="http://127.0.0.1:8200" vault-dev vault kv put secret/my-app password="HelloFromCloudVaultVM!"
  EOT
}
