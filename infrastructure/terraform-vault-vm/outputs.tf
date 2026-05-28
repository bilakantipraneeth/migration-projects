output "vault_public_ip" {
  description = "The public IP address of the Vault server"
  value       = google_compute_instance.vault_vm.network_interface[0].access_config[0].nat_ip
}

output "vault_url" {
  description = "The full HTTP URL to access Vault"
  value       = "http://${google_compute_instance.vault_vm.network_interface[0].access_config[0].nat_ip}:8200"
}
