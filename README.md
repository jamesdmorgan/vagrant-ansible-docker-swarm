# vagrant-ansible-docker-swarm
Initialising a Docker 1.12+ swarm cluster with Vagrant, Ansible &amp; Docker

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

## The swarm
After the boxes have been provisioned via Ansible the swarm is ready for containers

```bash
[root@manager1 vagrant]# docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
3ga8exh7uonx35nstda9d2tzd    manager2  Ready   Active        Reachable
4vpyb82xlnn9z4ax22we7kied    worker2   Ready   Active
8xr37ecimhrov0pddwudu6qxz    worker1   Ready   Active
bcbmos2eaatri4sn080tks2oi    manager3  Ready   Active        Reachable
bxcipvv74o4ontcr8jbh92dw6 *  manager1  Ready   Active        Leader
```
