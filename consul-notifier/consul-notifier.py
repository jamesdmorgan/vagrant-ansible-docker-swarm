#!/usr/bin/python
import sys
import logging
import docker
import consul
import re

logger = logging.getLogger(__name__)

# docker run -v /var/run/docker.sock:/var/run/docker.sock consul-notifier

# Communicating with consul

# http://gliderlabs.com/blog/2015/04/14/docker-events-explained/
status_map = {"stop": "stop", "die": "stop", "start": "start"}


def setup_logging(verbose=False):
    '''
    Setup logging

    :param verbose: bool - Enable verbose debug mode
    '''

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    if verbose:
        logger.setLevel(logging.DEBUG)


def start(cli, con, event):
    '''
    {
        'status': 'start',
        'timeNano': 1471291489261243761,
        'from': 'lucj/demo-www:1.0',
        'Actor': {
            'Attributes': {
                'com.docker.swarm.task': '',
                'name': 'www.8.e7nt85x8f6tic0tiow5wzv5z8',
                'com.docker.swarm.node.id': '2wzelo3sj0oowbuo2jxc9jcje',
                'image': 'lucj/demo-www:1.0',
                'com.docker.swarm.service.id': '5m24m676zm1q6tjdte2o06ieb',
                'com.docker.swarm.task.name': 'www.8',
                'com.docker.swarm.service.name': 'www',
                'com.docker.swarm.task.id': 'e7nt85x8f6tic0tiow5wzv5z8'
            },
            'ID': u'8217cb8565dd774f316c3e51b0f88551e3337edffb087f28db75fb7126160641'
        },
        'time': 1471291489,
        'Action': u'start',
        'Type': 'container',
        'id': '8217cb8565dd774f316c3e51b0f88551e3337edffb087f28db75fb7126160641'
    }

    '''

    swarm_name = event['Actor']['Attributes']['com.docker.swarm.service.name']
    print (event)

    container = cli.inspect_container(event['Actor']['Attributes']['name'])
    env = container['Config']['Env']

    port = 80
    for nv in env:
        n, v = str(nv).split('=')
        if n == 'CONSUL_SERVICE_PORT':
            port = v

    container_id = container['Name']

    logger.info("Registering {0} {1} port {2}".format(
        swarm_name, container_id, port))

    res = con.agent.service.register(
        swarm_name,
        service_id=container_id,
        port=80)

    if not res:
        logger.error("Failed to register service")

    for x in con.agent.services():
        print(x)


def stop(cli, con, event):
    swarm_name = event['Actor']['Attributes']['com.docker.swarm.service.name']
    print (event)

    container = cli.inspect_container(event['Actor']['Attributes']['name'])
    container_id = container['Name']

    logger.info("De-registering {0} {1}".format(swarm_name, container_id))
    res = con.agent.service.deregister(service_id=container_id)

    if not res:
        logger.error("Failed to de-register service")

    for x in con.agent.services():
        print(x)


def main():
    setup_logging(True)
    logger.info("Initialising")
    thismodule = sys.modules[__name__]

    # create a docker client object that talks to the local docker daemon
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    con = consul.Consul()

    # start listening for new events
    events = cli.events(decode=True)

    # possible events are:
    #  attach, commit, copy, create, destroy, die, exec_create, exec_start, export,
    #  kill, oom, pause, rename, resize, restart, start, stop, top, unpause, update
    for event in events:
        action = event['Action']
        if action in status_map:
            # if a handler for this event is defined, call it
            if (hasattr(thismodule, status_map[action])):
                getattr(thismodule, status_map[action])(cli, con, event)

if __name__ == '__main__':
    main()

