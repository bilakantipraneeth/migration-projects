variable "project_id" {
  description = "The GCP Project ID for the Prod Environment"
  type        = string
}

variable "secrets" {
  description = "The list of secrets to deploy in Prod"
  type = map(object({
    labels = map(string)
  }))
}
