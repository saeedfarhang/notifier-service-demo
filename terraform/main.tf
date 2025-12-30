terraform {
  required_version = ">=1.3.0"

  required_providers {
    arvan = {
      source = "terraform.arvancloud.ir/arvancloud/iaas"
      version = "~>0.8.1"
    }
  }
}

provider "arvan" {
  api_key = var.arvan_api_key
}
