variable "region" {
  type        = string
  description = "ArvanCloud region"
  default     = "ir-thr-fr1"
}

variable "ssh_key_name" {
  type        = string
  description = "Existing SSH key name in ArvanCloud"
  default     = "horcrux"
}

variable "flavor_id" {
  description = "Arvan plan ID for DevStack VM"
  type        = string
  default     = "g1-12-4-0"
}

variable "disk_size" {
  description = "Root disk size in GB"
  type        = number
  default     = 25
}

variable "enable_init_script" {
  description = "Whether to inject cloud-init to prep DevStack (packages, user, clone)"
  type        = bool
  default     = false
}

variable "auto_run_stack" {
  description = "Run ./stack.sh automatically during cloud-init (long running). Leave false for manual run."
  type        = bool
  default     = false
}

variable "devstack_password" {
  description = "Password for ADMIN/DATABASE/RABBIT/SERVICE in local.conf"
  type        = string
  default     = "secret"
  sensitive   = true
}

variable "devstack_branch" {
  description = "DevStack git branch to clone"
  type        = string
  default     = "master"
}

variable "arvan_api_key" {
  type        = string
  description = "ArvanCloud API key"
}

variable "security_group_ids" {
  description = "List of security group IDs to attach (use IDs, not names)"
  type        = list(string)
  default     = ["dec3e429-1559-46eb-b735-59db84665f8f"]
}