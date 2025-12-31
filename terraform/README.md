# Terraform – ArvanCloud DevStack Host

## Purpose

This Terraform project provisions the base IaaS resources on ArvanCloud required to host a **single-node DevStack (OpenStack) environment**.

### What Terraform does

- Creates a virtual machine on ArvanCloud
- Selects a compatible Linux image
- Injects a cloud-init script that:
  - Installs base packages and creates the `stack` user
  - Clones DevStack and writes `local.conf` with your secrets
  - Optionally runs `./stack.sh` if you permit it

### What Terraform does not do (unless you opt in)

- Running `./stack.sh` can be long; keep `auto_run_stack=false` if you prefer to run it manually after SSH.
- Deploy application-level services beyond DevStack

## Directory Structure

terraform/
├── main.tf # Terraform settings and provider
├── variables.tf # Input variables
├── data.tf # Image lookup
├── vm.tf # VM and networking resources
└── README.md

## Usage

```bash
terraform init
terraform apply \
  -var arvan_api_key=... \
  -var devstack_password=... \
  -var auto_run_stack=false   # set true to run stack.sh during cloud-init (long)
```

## Variables

- `enable_init_script` (bool, default: true): injects the cloud-config bootstrap.
- `devstack_password` (sensitive, default: "secret"): used for ADMIN/DATABASE/RABBIT/SERVICE in `local.conf`.
- `devstack_branch` (default: "master"): git branch of DevStack to clone.
- `auto_run_stack` (bool, default: true): if true, cloud-init runs `./stack.sh` (long-running). Set to false to keep apply fast and run manually.

Pass variables via `-var` or a `terraform.tfvars` file; keep secrets out of VCS.
