# vagrant-ansible-docker-swarm
Initialising a Docker swarm cluster with Vagrant, Ansible &amp; Docker 1.12

## Overview

![swarm diagram](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/blob/master/images/diagrams/swarm.png:wq)

### [Current status](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/blob/master/CHANGELOG.md#current-status)

### Components

- **Vagrant** - Management of Virtualbox VMs
- **Ansible** - Provisioning of boxes
- **Docker 1.12** - Swarm creation on manager and worker boxes
- **Consul** - External DNS, K/V store and dashboard
- **Registrator** - Intended to register services [but doesn't currently work](https://github.com/gliderlabs/registrator/issues/443) with **1.12**
- **Consul-notifier** - Temporary replacement to **Registrator** for registering services

## Vagrant
I have chosen to tie everything together using Vagant and Ansible. I could have used Docker Machine to create
a cluster of boxes and shell scripts to initialise the swarm but I feel that Ansible is a cleaner solution.

In a production environment the Ansible scripts can still be used alongside cloudformation or terraform.

Using multiple named ansible provisioners means that I can iteratively build up the system. Each Ansible
playbook will handle a different section. I.e docker swarm, monitoring, applications etc.

As the docker swarm is the underlying framework that everything will run on it is the default provisioner

To run the different provisioners run vagrant using the following command

```bash
$ vagrant provision --provision-with monitoring
```

## Ansible
The demo uses the latest version of Ansible v2.1 for the [docker service](https://docs.ansible.com/ansible/docker_service_module.html) module. Unfortunately this is currently [incompatible](https://github.com/docker/docker/issues/24107) with Docker Swarm due to docker-service using Docker compose behind the scenes. Hopefully this will be resolved soon as it provides more resilient idempotency and doesn't require searching the output of the **docker service** command.

To speed up the development process its easy to run the Ansible provisioning directly from the root of the project directory

If you use the following alias then you just need to provide the playbook

```bash
alias ansible-vagrant='PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true ANSIBLE_HOST_KEY_CHECKING=false ANSIBLE_SSH_ARGS='\''-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes -o ControlMaster=auto -o ControlPersist=60s'\'' ansible-playbook --connection=ssh --timeout=30 --inventory-file=.vagrant/provisioners/ansible/inventory'
```

Using the Ansible docker modules handles reloading containers. This means that when you change the source for a container, Ansible will rebuild and reload it.

```bash
$ ansible-vagrant ansible/apps.yml -vv
No config file found; using defaults

PLAYBOOK: apps.yml *************************************************************
1 plays in ansible/apps.yml

PLAY [managers[0]] *************************************************************

TASK [setup] *******************************************************************
ok: [manager1]
...
```

## Docker Swarm
After the boxes have been provisioned via Ansible the swarm is ready for containers.

The demo uses 3 small manager boxes. I want to build a system that is as close to a production setup that
can run on a laptop. Its important that all applications including the swarm are highly available.
The swarm managers need an odd number of boxes to correctly achieve quorum. The current docker [documentation](https://docs.docker.com/swarm/plan-for-production/) is pre 1.12 and external service discovery. This is handled in 1.12 by the docker engine.

**update** Temporarily reduced managers & workers as hit performance issues with low specced boxes. 2 CPU/ 2Gb works

As consul is used for other tasks other than service discovery. DNS, k/v store and health checking I will add it to
the demo along with registrator. I'll continue to use the docker engine swarm for load balancing and service discovery unless
consul brings benefit in this area

There are currently two worker boxes though this can be scaled out depending on the host machines specs.

```bash
[root@manager1 vagrant]# docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
3ga8exh7uonx35nstda9d2tzd    manager2  Ready   Active        Reachable
4vpyb82xlnn9z4ax22we7kied    worker2   Ready   Active
8xr37ecimhrov0pddwudu6qxz    worker1   Ready   Active
bcbmos2eaatri4sn080tks2oi    manager3  Ready   Active        Reachable
bxcipvv74o4ontcr8jbh92dw6 *  manager1  Ready   Active        Leader
```

## Applications
At this stage of the project I just want to have a couple of services communicating over the distributed swarm. The blog post [Deploy a multi services application with swarm mode](http://lucjuggery.com/blog/?p=604) by Luc Juggery has a nice clear example that I have incorporated to demonstrate the swarm. This will provide a means to start testing the system monitoring that will be added later in the project. When this is in place i'll look to add my own applications.
