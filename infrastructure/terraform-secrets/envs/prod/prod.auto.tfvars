project_id = "my-prod-gcp-project"

secrets = {
  "prod-database-password" = {
    labels = { environment = "prod", component = "database" }
  }
  "prod-api-key" = {
    labels = { environment = "prod", component = "backend" }
  }
}
