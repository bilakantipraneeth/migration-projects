variable "project_id" {
  description = "The GCP Project ID for the Dev Environment"
  type        = string
}

variable "secrets" {
  description = "The list of secrets to deploy in Dev"
  type = map(object({
    labels = map(string)
  }))
}
