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
