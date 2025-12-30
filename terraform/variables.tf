variable "region" {
  type        = string
  description = "ArvanCloud region"
  default     = "ir-thr-ba1"
}

variable "ssh_key_name" {
  type        = string
  description = "Existing SSH key name in ArvanCloud"
  default     = "horcrux"
}

variable "flavor_id" {
  description = "Arvan plan ID for DevStack VM"
  type        = string
  default     = "g4-16-6-0"
}

variable "disk_size" {
  description = "Root disk size in GB"
  type        = number
  default     = 25
}

variable "arvan_api_key" {
  type        = string
  description = "ArvanCloud API key"
}

variable "security_group_ids" {
  description = "List of security group IDs to attach (use IDs, not names)"
  type        = list(string)
  default     = ["75090bfa-7ab7-40b2-845e-af25171bb779"]
}