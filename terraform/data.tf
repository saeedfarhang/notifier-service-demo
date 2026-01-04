data "arvan_images" "image_list" {
	region = var.region
	image_type = "distributions"
}

locals {
	ubuntu_2204 = [
		for img in data.arvan_images.image_list.distributions :
		img if img.distro_name == "ubuntu" && img.name == "22.04"
	][0]
}

data "arvan_plans" "plan_list" {
  region = var.region
}

data "arvan_security_groups" "default_security_groups" {
  region = var.region
}

# output "plan_list" {
#   value = data.arvan_plans.plan_list
# }
# output "security_groups" {
#   value = data.arvan_security_groups.default_security_groups
# }
