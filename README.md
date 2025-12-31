# OpenStack Event Notifier on ArvanCloud IaaS

Minimal demo for the interview challenge: provision a single-node DevStack on ArvanCloud and push OpenStack events (compute lifecycle) to email with metrics exposure.

## Repo layout

- `terraform/` -- provisions the VM on ArvanCloud; optional cloud-init to prep DevStack and optionally run `stack.sh`.
- `devstack/` -- manual setup notes and `local.conf` reference.
- `notifier/` -- Python service that consumes RabbitMQ notifications, filters event types, sends email, and exposes Prometheus metrics.

## What this delivers

- Arvan VM ready for DevStack.
- DevStack with RabbitMQ notifications enabled (standard topics).
- Notifier service that watches `notifications.*`, filters allowed events, emails admin, and exposes counters.

## Prerequisites

- Terraform ≥ 1.3, ArvanCloud API key with IaaS access.
- SSH key already registered in ArvanCloud.
- SMTP creds (or leave email disabled for dry runs).

## Quick start

1. **Provision VM**

```bash
cd terraform
terraform init
terraform apply \
  -var arvan_api_key=... \
  -var devstack_password=... \
  -var auto_run_stack=false   # set true to run ./stack.sh during cloud-init (long)
```

Outputs include the floating IP (`devstack_floating_ip`).

2. **Finish DevStack (if auto_run_stack=false - default)**

refer to [Setup DevStack](./devstack/setup.md) for finishing DevStack Setup.

Validate: `source openrc admin admin && openstack service list`

3. **Run notifier**

```bash
cd notifier
python -m venv env && source env/bin/activate
pip install -r requirements.txt
python -m cmd.notifier.main configs/config.yaml
```

Adjust `configs/config.yaml` for RabbitMQ URL, routing keys, allowed events, and SMTP settings. Metrics default to `:9000/metrics`.

## Triggering a demo event

- Create or delete a VM in Horizon/CLI to emit `compute.instance.create.end` or `compute.instance.create.error`.

> for cli:
>
> ```bash
> openstack server create \
>   --image cirros \
>   --flavor m1.tiny \
>   --network private \
>   test-vm
> ```

- Watch notifier logs for the event and check your inbox (or observe metrics counters if email disabled).

## Notes

- Ensure ports for SSH, Horizon, RabbitMQ (if needed), and notifier metrics are allowed.
