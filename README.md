# vagrant-ansible-docker-swarm
Initialising a Docker swarm cluster with Vagrant, Ansible &amp; Docker 1.12

## Current status
* Vagrant spins up 5 virtual box machines, 3 managers for quorum & 2 workers
* The memory footprint is pretty small until I have add more memory to my machine...
* Ansible provisions the boxes installing docker 1.12
* The primary manager starts the swarm cluster, each other manager and worker then joins
* The status of the swarm is outputted at the end
* Installation of docker & initialisation of the swarm is idempotent so provision can be re-run
    * This can be replaced when there are Ansible modules for managing swarm.

## Next steps
* Start simple flask & nginx containers as services using v2 docker compose
* Add multiple overlay networks for front and backend
* Investigate host / container monitoring
* Investigate running shipyard for visualisation

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

## The swarm
After the boxes have been provisioned via Ansible the swarm is ready for containers.

The demo uses 3 small manager boxes. I want to build a system that is as close to a production setup that
can run on a laptop. Its important that all applications including the swarm are highly available.
The swarm managers need an odd number of boxes to correctly achieve quorum. The current docker [documentation](https://docs.docker.com/swarm/plan-for-production/) is pre 1.12 and external service discovery. This is handled in 1.12 by the docker engine.

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
