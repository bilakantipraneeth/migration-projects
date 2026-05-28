project_id = "my-dev-gcp-project"

secrets = {
  "dev-database-password" = {
    labels = { environment = "dev", component = "database" }
  }
  "dev-api-key" = {
    labels = { environment = "dev", component = "backend" }
  }
}
