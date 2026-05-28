output "created_secrets" {
  description = "The names of the created secret shells"
  value       = [for s in google_secret_manager_secret.secret_shells : s.secret_id]
}

output "secret_ids" {
  description = "The full IDs of the created secrets"
  value       = [for s in google_secret_manager_secret.secret_shells : s.id]
}
