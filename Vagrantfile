# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Scientific Linux 6.4
  config.vm.box = "SLC-6.4"

  config.vm.box_url = "http://lyte.id.au/vagrant/sl6-64-lyte.box"

  # Forward port 5000 from the VM to the host
  config.vm.network :forwarded_port, guest: 5000, host: 5000

  # Provision the VM using the root_provisioning shell script
  config.vm.provision "shell", path: "root_provisioning.sh"
end
