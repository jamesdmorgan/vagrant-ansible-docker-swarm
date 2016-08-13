# Change Log

## Current status
- Vagrant spins up 5 virtual box machines, 3 managers for quorum & 2 workers
- The memory footprint is pretty small until I have add more memory to my machine...
- Ansible provisions the boxes installing docker 1.12
- The primary manager starts the swarm cluster, each other manager and worker then joins
- The status of the swarm is outputted at the end
- Installation of docker & initialisation of the swarm is idempotent so provision can be re-run
- This can be replaced when there are Ansible modules for managing swarm.
- Start collection of services to test the swarm
- multiple overlay networks for front and backend

## Future
- Add monitoring, investigate
    - cAdvisor for docker stats
    - collectd
    - statsd for udp from applications
    - influxdb
    - grafana

- Add shipyard for visualisation
- Add consul for external dns resolution and healthchecks (container or physical?)
- Consider [Alpine](https://github.com/maier/vagrant-alpine) vagrant box for workers as only running Docker

## Unreleased [0.2](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/releases/tag/v0.2) (2016-08-14)

** Added:**
- Addded node labels manager and worker so we can restrict where services are run

## [0.1](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/releases/tag/v0.1) (2016-08-11)

**Added:**
- Added multi-provisioner, multi-box Vagrant file to spin up Docker swarm managers and workers
- Added Ansible provisioning swarm.yml to bootstap managers and workers
- Added apps.yml playbook to start up a collection of demo containers to demonstrate swarm

**Known Issues**
- docker service rm seems to leave containers in /dev/mapper causing very high i/o wait
