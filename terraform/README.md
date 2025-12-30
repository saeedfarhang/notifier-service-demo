# Terraform – ArvanCloud Demo

## Purpose

This Terraform project provisions the **base IaaS resources on ArvanCloud** required to host a **single-node DevStack (OpenStack) environment**.

---

## Scope

### What Terraform does

- Creates a virtual machine on ArvanCloud
- Selects a compatible Linux image

### What Terraform does not do

- Install or configure DevStack / OpenStack
- Run cloud-init or bootstrap scripts
- Deploy OpenStack services or applications

OpenStack setup is performed manually after provisioning.

---

## Why DevStack Is Installed Manually

Due to **cloud-init execution limitations** and to keep provisioning deterministic, DevStack installation is intentionally excluded from Terraform.

---

## Directory Structure

terraform/
├── main.tf # Terraform settings and provider
├── variables.tf # Input variables
├── data.tf # Image lookup
├── vm.tf # VM and networking resources
└── README.md

---

## Usage

```bash
terraform init
terraform plan
terraform apply
```
