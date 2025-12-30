resource "arvan_abrak" "devstack" {
    name = "devstack-lab"
    timeouts {
        create = "1h30m"
        update = "2h"
        delete = "20m"
        read   = "10m"
    }
    region = var.region
    image_id = local.ubuntu_2204.id
    flavor_id = var.flavor_id
    disk_size = var.disk_size
    enable_ipv4 = true
    enable_ipv6 = false
    security_groups = var.security_group_ids
    ssh_key_name = var.ssh_key_name
}

output "instances" {
  value = arvan_abrak.devstack
}
