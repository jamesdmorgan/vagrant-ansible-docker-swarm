# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant 1.7+ automatically inserts a different
# insecure keypair for each new VM created. The easiest way
# to use the same keypair for all the workers is to disable
# this feature and rely on the legacy insecure key.
# config.ssh.insert_key = false
#
# Note:
# As of Vagrant 1.7.3, it is no longer necessary to disable
# the keypair creation when using the auto-generated inventory.

VAGRANTFILE_API_VERSION = "2"
MANAGERS = 3
WORKERS = 2

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "tsihosting/centos7"

  config.vm.provider 'virtualbox' do |v|
    v.linked_clone = true if Vagrant::VERSION =~ /^1.8/
  end

  config.ssh.insert_key = false

  (1..MANAGERS).each do |manager_id|
    config.vm.define "manager#{manager_id}" do |manager|
      manager.vm.hostname = "manager#{manager_id}"
      manager.vm.network "private_network", ip: "192.168.77.#{20+manager_id}"
      manager.vm.provider "virtualbox" do |v|
        v.memory = 512
        v.cpus = 1
      end
    end
  end

  (1..WORKERS).each do |worker_id|
    config.vm.define "worker#{worker_id}" do |worker|
      worker.vm.hostname = "worker#{worker_id}"
      worker.vm.network "private_network", ip: "192.168.77.#{30+worker_id}"
      worker.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 1
      end

      # Only execute once the Ansible provisioner,
      # when all the workers are up and ready.
      if worker_id == WORKERS
        worker.vm.provision :ansible do |ansible|
          # Disable default limit to connect to all the workers
          ansible.limit = "all"
          ansible.playbook = "ansible/provision.yml"
          ansible.verbose = "vv"
          ansible.groups = {
            "managers" => ["manager[1:#{MANAGERS}]"],
            "workers" => ["worker[1:#{WORKERS}]"],
            "all_groups:children" => ["managers", "workers"]
          }
        end
      end
    end
  end
end
