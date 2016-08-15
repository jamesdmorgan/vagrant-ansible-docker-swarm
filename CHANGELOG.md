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
- Clustered consul servers and nodes on all hosts

## Future
- Add monitoring, investigate
    - cAdvisor for docker stats
    - collectd
    - statsd for udp from applications
    - influxdb
    - grafana

- Add shipyard for visualisation
- Consider [Alpine](https://github.com/maier/vagrant-alpine) vagrant box for workers as only running Docker

## [0.3] Unreleased

**Issues:**
- Registrator does not work with 1.12 and service events
    Possible temporary solution is to have a cron on each node and poll the docker daemon for events

    ```bash
    echo -e "GET /events?since=1471083135 HTTP/1.0\r\n" | nc -U /var/run/docker.sock
    ```

    The docker API returns newline delimited JSON which can be parsed using [NewlineJson](https://pypi.python.org/pypi/NewlineJSON/1.0)

    This information can then be used to update consul for stopped and started apps

    ```bash
    /v1/agent/service/deregister/<serviceId>
    /v1/agent/service/register/<serviceId>
    ```

## [0.2](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/releases/tag/v0.2) (2016-08-13)

**Added:**
- Restrict services to worker nodes using constraint filter
- Added clustered consul docker container to each machine
    - All provisioned with Ansible
    - 3 servers on each manager
    - 3 nodes on each worker
    - UI available at http://192.168.77.21:8500/ui
    - DNS available at dig @172.17.0.1 -p 53 manager2.node.consul

## [0.1](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/releases/tag/v0.1) (2016-08-11)

**Added:**
- Added multi-provisioner, multi-box Vagrant file to spin up Docker swarm managers and workers
- Added Ansible provisioning swarm.yml to bootstap managers and workers
- Added apps.yml playbook to start up a collection of demo containers to demonstrate swarm

**Known Issues**
- docker service rm seems to leave containers in /dev/mapper causing very high i/o wait
