# Change Log

## Current status
- Vagrant spins up 6 virtual box machines, 3 managers for quorum & 3 workers
- Ansible provisions the boxes installing docker 1.12
- The primary manager starts the swarm cluster, each other manager and worker then joins
  - The status of the swarm is outputted at the end
- Installation of docker & initialisation of the swarm is idempotent so provision can be re-run
  - Use of shell can be replaced when there are Ansible modules for managing swarm.
- Start collection of services to test the swarm
- multiple overlay networks for front and backend
- Clustered consul servers and nodes on all hosts
- Centralised logging via syslog docker log driver feeding into ELK stack
  - Will publish all the endpoints

- Host monitoring using collectd -> riemann -> influxdb -> grafana.

## Roadmap
- Add monitoring, investigate
    - [cAdvisor](https://github.com/google/cadvisor) for docker stats
    - collectd
    - [Riemann tools](https://github.com/riemann/riemann-tools) for Docker & Consul
    - statsd for udp from applications (though Riemann.io recommend against UDP)

- Add shipyard for visualisation
- Consider [Alpine](https://github.com/maier/vagrant-alpine) vagrant box for workers as only running Docker

- [Generate](https://galaxy.ansible.com/ansible/secure-docker-daemon/) ca & certs so we can connect to the manager1 daemon from other boxes.
- Update systemd docker [file](https://docs.docker.com/engine/admin/systemd/) on manager1 so we can start the daemon with TCP/TLS support

- Look to start daemon running on 2375 https://docs.docker.com/v1.10/engine/reference/commandline/daemon/

- Add multiple overlay networks and pull out hardcoded **appnet** configuration

## [0.4](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/releases/tag/v0.4) (2016-08-26) Monitoring

**Added:**

- Added monitoring ansible playbook
- Added global collectd container service
- Added [influxdb](https://influxdata.com/) service constrained to influx ansible group
- Added single instance of [Riemann](http://riemann.io). H/A is [complicated](https://groups.google.com/forum/m/#!topic/riemann-users/pkMk0aWIjqo)
- Added [grafana](https://grafana.net/) service including influxdb datasource and demo dashboard for CPU - needs work

## [0.3](https://github.com/jamesdmorgan/vagrant-ansible-docker-swarm/releases/tag/v0.3) (2016-08-20) Logging and Consul

**Added:**
- Created python script that utilises **docker-py** and **python-consul** to listen for docker start/stop events
and register/de-register with consul. The script runs inside an Alpine python container on each node in the cluster.

    By default the container listens to the stream. You can manually register/deregister by passing args to the script

    ```bash
    /app # [root@worker1 vagrant]# docker exec -it $(cname consul-notifier) /bin/ash
    /app # python consul-notifier.py -a register -n consul-notifier
    [2016-08-18 12:18:13,374] Consul notifier processing register
    [2016-08-18 12:18:13,377] Registering consul-notifier worker1:consul-notifier:80 port 80
    /app # python consul-notifier.py -a deregister -n consul-notifier
    [2016-08-18 12:18:18,184] Consul notifier processing deregister
    [2016-08-18 12:18:18,188] De-registering consul-notifier worker1:consul-notifier:80
    ```

- Added logging.yml and monitoring.yml and Vagant ansible invocations.
- Added rsyslog Ansible for all boxes
- Added syslog driver and [tags](https://docs.docker.com/engine/admin/logging/log_tags/) to consul-notifier
- Added syslog to all services
- Added rudimentary ELK stack on 2nd Manager box
    - rsyslog runs on every box and forwards messages to logstash -> elasticsearch -> kibana on Manager2


**Issues:**

- Registrator does not work with 1.12 and service events **Address above**

    Possible temporary solution is to have a container on each node and poll the docker daemon for events

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
