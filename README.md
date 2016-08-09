# vagrant-ansible-docker-swarm
Initialising a Docker swarm cluster with Vagrant, Ansible &amp; Docker

## Current status
* Vagrant spins up 5 virtual box machines, 3 managers for quorum & 2 workers
* The memory footprint is pretty small until I have add more memory...
* Ansible provisions the boxes installing docker 1.12
* The primary manager starts the swarm cluster each other manager and worker then joins
* The status of the swarm is outputted at the end
* Installation of docker & initialisation of the swarm is idempotent so provision can be re-run
** This can be replaced when there are Ansible modules for managing swarm.

## Next steps
* Start simple flask & nginx containers as services using v2 docker compose
* Add multiple overlay networks for front and backend
* Investigate host / container monitoring
* Investigate running shipyard for visualisation

