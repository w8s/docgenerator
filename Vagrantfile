# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu-14.04-amd64-vbox"
  config.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider "virtualbox" do |vb|
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provision "shell", inline: "apt-get update"
  #config.vm.provision "shell", inline: "apt-get -y upgrade"

  config.vm.provision "shell", inline: "apt-get --no-install-recommends install -y python-setuptools build-essential python-dev"

  config.vm.provision "shell", inline: "easy_install pip"

  config.vm.provision "shell", inline: "pip install -r /vagrant/requirements.txt"

end
