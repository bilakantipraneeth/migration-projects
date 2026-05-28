variable "project_id" {
  description = "The GCP Project ID where the secrets will be created"
  type        = string
}

variable "secrets" {
  description = "A map of secret names and their configurations"
  type = map(object({
    labels = map(string)
  }))
  default = {
    "my-app-secret-1" = {
      labels = { environment = "dev" }
    }
  }
}
