# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'etc'

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
 config.vm.box = "fedora/30-cloud-base"

# Forward traffic on the host to the development server on the guest
# config.vm.network "forwarded_port", guest: 5000, host: 5000
 # RabbitMQ
 config.vm.network "forwarded_port", guest: 15672, host: 15672

 if Vagrant.has_plugin?("vagrant-hostmanager")
     config.hostmanager.enabled = true
     config.hostmanager.manage_host = true
 end

 # Vagrant can share the source directory using rsync, NFS, or SSHFS (with the vagrant-sshfs
 # plugin). By default it rsyncs the current working directory to /vagrant.
 #
 # If you would prefer to use NFS to share the directory uncomment this and configure NFS
 # config.vm.synced_folder ".", "/vagrant", type: "nfs", nfs_version: 4, nfs_udp: false
 config.vm.synced_folder ".", "/vagrant", disabled: true
 config.vm.synced_folder ".", "/home/vagrant/devel", type: "sshfs"

 # To cache update packages (which is helpful if frequently doing `vagrant destroy && vagrant up`)
 # you can create a local directory and share it to the guest's DNF cache. The directory needs to
 # exist, so create it before you uncomment the line below.
 #
 # config.vm.synced_folder ".dnf-cache", "/var/cache/dnf", type: "sshfs", sshfs_opts_append: "-o nonempty"

 # Comment this line if you would like to disable the automatic update during provisioning
 config.vm.provision "shell", inline: "sudo dnf upgrade -y"

 # Create the "mbbox" OpenShift 3.11 box
 config.vm.define "mbbox_os311", primary: true do |mbbox_os311|
    mbbox_os311.vm.host_name = "mbbox-os311.example.com"
    # bootstrap and run with ansible
    mbbox_os311.vm.provision "ansible" do |ansible|
      ansible.playbook = "ci/mbbox-os311-playbook.yml"
      ansible.raw_arguments = ["-e", "ansible_python_interpreter=/usr/bin/python3"]
    end

    mbbox_os311.vm.provider :libvirt do |domain|
        # Season to taste
        domain.cpus = Etc.nprocessors
        domain.cpu_mode = "host-passthrough"
        domain.graphics_type = "spice"
        domain.memory = 4096
        domain.video_type = "qxl"

        # Uncomment the following line if you would like to enable libvirt's unsafe cache
        # mode. It is called unsafe for a reason, as it causes the virtual host to ignore all
        # fsync() calls from the guest. Only do this if you are comfortable with the possibility of
        # your development guest becoming corrupted (in which case you should only need to do a
        # vagrant destroy and vagrant up to get a new one).
        #
        # domain.volume_cache = "unsafe"
    end
 end
 
 # Create the "mbbox" OperatorSDK box
 config.vm.define "mbbox_osdk", autostart: false do |mbbox_osdk|
    mbbox_osdk.vm.host_name = "mbbox-osdk.example.com"
    # bootstrap and run with ansible
    mbbox_osdk.vm.provision "ansible" do |ansible|
      ansible.playbook = "ci/mbbox-osdk-playbook.yml"
      ansible.raw_arguments = ["-e", "ansible_python_interpreter=/usr/bin/python3"]
    end

    mbbox_osdk.vm.provider :libvirt do |domain|
        # Season to taste
        domain.cpus = Etc.nprocessors
        domain.cpu_mode = "host-passthrough"
        domain.graphics_type = "spice"
        domain.memory = 4096
        domain.video_type = "qxl"

        # Uncomment the following line if you would like to enable libvirt's unsafe cache
        # mode. It is called unsafe for a reason, as it causes the virtual host to ignore all
        # fsync() calls from the guest. Only do this if you are comfortable with the possibility of
        # your development guest becoming corrupted (in which case you should only need to do a
        # vagrant destroy and vagrant up to get a new one).
        #
        # domain.volume_cache = "unsafe"
    end
 end
end
