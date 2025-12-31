#cloud-config
package_update: true
package_upgrade: true
packages:
  - git
  - curl
  - python3
  - python3-pip
  - sudo
runcmd:
  - |
    exec > >(tee -a /var/log/devstack-bootstrap.log) 2>&1
    set -euxo pipefail

    echo "[bootstrap] ensure stack user"
    id stack || useradd -s /bin/bash -d /opt/stack -m stack
    chmod +x /opt/stack
    echo "stack ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/stack
    chmod 440 /etc/sudoers.d/stack

    echo "[bootstrap] clone devstack (branch ${DEVSTACK_BRANCH})"
    su - stack -c "cd /opt/stack && ( [ -d devstack ] || git clone --branch \"${DEVSTACK_BRANCH}\" https://opendev.org/openstack/devstack )"

    echo "[bootstrap] write local.conf"
    su - stack -c "cd /opt/stack/devstack && cat > local.conf <<'LOCALCONF'
[[local|localrc]]
ADMIN_PASSWORD=${DEVSTACK_PASSWORD}
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
HOST_IP=$(ip -4 addr show scope global | awk '/inet / {print $2}' | cut -d/ -f1 | head -n1)
LOCALCONF
"

    if [ \"${AUTO_RUN_STACK}\" = \"true\" ]; then
      echo \"[bootstrap] running stack.sh (long)\" 
      su - stack -c "cd /opt/stack/devstack && ./stack.sh"
    else
      echo \"[bootstrap] skipping stack.sh (auto_run_stack=false)\"
    fi

