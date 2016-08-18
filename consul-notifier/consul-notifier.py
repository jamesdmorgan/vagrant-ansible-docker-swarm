#!/usr/bin/python
import argparse
import json
import sys
import logging
import docker
import consul

logger = logging.getLogger(__name__)
args = None

# docker run -v /var/run/docker.sock:/var/run/docker.sock consul-notifier

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


class Service(object):

    def __init__(self, cli, con, name):

        # http://gliderlabs.com/blog/2015/04/14/docker-events-explained/
        self.status_map = {
            "stop": "deregister",
            "die": "deregister",
            "start": "register",
            "register": "register",
            "deregister": "deregister"
        }

        self.con = con
        self.name = name
        self.container = cli.inspect_container(name)
        self.env = self.container['Config']['Env']
        self.hostname = self.container['Config']['Hostname']
        self.port = self.get_port(80)

        # Strip the leading slash
        self.container_name = self.container['Name'][1:]
        self.container_id = self.get_id()

        if args.verbose:
            print(json.dumps(self.container, sort_keys=True, indent=4))

    def get_port(self, default):
        for nv in self.env:
            n, v = str(nv).split('=')
            if n == 'CONSUL_SERVICE_PORT':
                return v

        return default

    def get_id(self):
        return "{0}:{1}:{2}".format(
            self.hostname,
            self.container_name,
            self.port)

    def handle(self, action):
        if (action in self.status_map and hasattr(self, self.status_map[action])):
            getattr(self, self.status_map[action])()
        else:
            logger.warning("Ignoring action {0}".format(action))

    def register(self):
        logger.info("Registering {0} {1} port {2}".format(
            self.name,
            self.container_id,
            self.port))

        res = self.con.agent.service.register(
            self.name,
            service_id=self.container_id,
            port=self.port)

        if not res:
            logger.error("Failed to register service")
            sys.exit(1)

    def deregister(self):
        logger.info("De-registering {0} {1}".format(
            self.name,
            self.container_id))

        res = con.agent.service.deregister(service_id=self.container_id)

        if not res:
            logger.error("Failed to de-register service")
            sys.exit(1)


def handler_args():

    global args

    help_text = '''
Register / De-register services manually or via Docker Daemon event stream
    '''

    parser = argparse.ArgumentParser(
        description=help_text,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--verbose', '-v', action="count", default=0,
                        help='Verbose Logging')

    parser.add_argument('--action', '-a', default='stream',
                        help='Notification action (stream, register, deregister)')

    parser.add_argument('--name', '-n', default=None,
                        help='Container Name')

    args = parser.parse_args()

    return args


def stream(cli, con):
    '''
    Connect to the docker daemon and listen for events
    possible events are:
        attach, commit, copy, create, destroy, die
        exec_create, exec_start, export, kill, oom, pause,
        rename, resize, restart, start, stop, top, unpause, update

        Example start dict
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

    # start listening for new events
    for event in cli.events(decode=True):

        name = event['Actor']['Attributes']['name']
        action = event['Action']

        print("-" * 80)
        print("Processing {0} event {1}".format(action, name))
        print (json.dumps(event, sort_keys=True, indent=4))
        print("-" * 80)

        s = Service(cli, con, name)
        s.handle(action)


def main():
    args = handler_args()
    setup_logging(args.verbose)

    # create a docker client object that talks to the local docker daemon
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    con = consul.Consul()

    logger.info("Consul notifier processing {0}".format(args.action))

    if args.action == 'stream':
        stream(cli, con)
    elif args.action in ['register', 'deregister']:
        s = Service(cli, con, args.name)
        s.handle(args.action)
    else:
        logger.error("Unknown action {0}".format(args.action))
        sys.exit(1)


if __name__ == '__main__':
    main()
