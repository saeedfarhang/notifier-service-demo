# DevStack Setup Guide

## Purpose

This document describes the **manual installation of a single-node DevStack environment**
used to demonstrate OpenStack infrastructure events for the notification service.

The setup is minimal and suitable for live demos.

---

## Environment

- Provider: ArvanCloud IaaS
- OS: Ubuntu 22.04 LTS
- Architecture: Single-node (all services on one VM)

---

## Pre-requisites

- Fresh VM provisioned via Terraform
- SSH access with sudo privileges
- Internet access from the VM

---

## System Preparation

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl python3 python3-pip
```

Disable conflicting firewall rules (demo environment only):

```bash
sudo ufw disable
```

## DevStack Installation

##### Create Stack User

```bash
sudo useradd -s /bin/bash -d /opt/stack -m stack
```

Ensure home directory for the stack user has executable permission for all, as RHEL based distros create it with 700 and Ubuntu 21.04+ with 750 which can cause issues during deployment.

```bash
sudo chmod +x /opt/stack
```

Since this user will be making many changes to your system, it should have sudo privileges:

```bash
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo su stack
cd /opt/stack
```

##### Download DevStack

```bash
git clone https://opendev.org/openstack/devstack

cd devstack
```

##### Configuration (local.conf)

A minimal configuration is used to enable only required services. create a file with `local.conf` name in devstack directory and put this:

```ini
[[local|localrc]]
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

HOST_IP=<VM_FLOATING_IP>
```

##### Start the install

```bash
./stack.sh
```

The installation may take 15–30 minutes.
After successful installation:

```bash
source openrc admin admin
openstack service list
openstack hypervisor list

```

Horizon dashboard should be available at: http://<VM_FLOATING_IP>/dashboard

## Event Infrastructure Validation

Verify that RabbitMQ is running and accessible:

```bash
sudo systemctl status rabbitmq-server
```

OpenStack services publish notifications to RabbitMQ topics such as:

- notifications
- notifications.info
- notifications.error

These topics are consumed by the external notification service.
