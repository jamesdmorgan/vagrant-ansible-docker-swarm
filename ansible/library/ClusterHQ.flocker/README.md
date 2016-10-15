# Ansible Role: Flocker Installer

[![Build Status](https://travis-ci.org/ClusterHQ/ansible-role-flocker.svg?branch=master)](https://travis-ci.org/ClusterHQ/ansible-role-flocker.svg?branch=master)

## Requirements

* Docker must be installed on all Flocker agent nodes.
* This role requires you install the Flocker Client on the machine running the ansible playbook.  Certificates are generated on the local machine (in `flocker_local_tempdir`) using flocker-ca and then distributed to the nodes. For more information see  [Installing the Flocker Client](https://docs.clusterhq.com/en/latest/flocker-standalone/install-client.html).
* The user must supply the path to a local agent.yml flocker file.

## Role Variables

    flocker_control_service_groupname: flocker_control_service
    
The name of an ansible host group that contains one host: the node hosting the flocker control service. The default value for this group name is flocker_control_serivce. If the host group is called something else, change this variable to match the host group name you've chosen.

    flocker_agents_groupname: flocker_agents

Similar to flocker_control_service_groupname but represents the groupname of the Flocker agent nodes.

    flocker_agent_yml_path: ""

The absolute path to an agent.yml file on the local ansible machine. For more information on creating agent.yml refer to Configuring the Nodes and Storage Backends https://docs.clusterhq.com/en/latest/flocker-standalone/configuring-nodes-storage.html

    flocker_cluster_name: my_flocker_cluster

The name of the cluster.  This name will be used when creating the cluster certificates and, in the default case, the directory on the local machine where copies of the certs and keys are created.

    # Warning: this folder will be deleted everytime the playbook is run
    flocker_local_tempdir: /tmp/{{ flocker_cluster_name }}

The path to a folder that will be used to generate the cluster certificates and keys.  This folder will not be cleaned up when the installation is finished.  However, the folder will be deleted and recreated at the start of every provisioning run.

    flocker_api_cert_name: api_user

A unique identifier for the API client.

    flocker_install_docker_plugin: True

Set to True to install the Flocker Plugin for Docker.

## Example Playbook

    ---
    - hosts: nodes
      user: ubuntu
      roles:
        - role: ClusterHQ.flocker

## Example Invocation

    ansible-playbook -i inventory/hosts flocker_example_playbook.yml  --extra-vars "flocker_agent_yml_path=/home/user/config_files/agent.yml"

## Example Inventory

    [flocker_control_service]
    computer1.example.com
    
    [flocker_agents]
    computer2.example.com
    computer3.example.com
    
    [nodes:children]
    flocker_control_service
    flocker_agents
    
## License

MIT / BSD
