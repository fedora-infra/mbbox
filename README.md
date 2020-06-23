[![Documentation Status](https://readthedocs.org/projects/mbbox-operator/badge/?version=latest)](https://mbbox-operator.readthedocs.io/en/latest/?badge=latest)

# mbox
Module Building in a Box

This repository contains a Kubernetes operator for deployment of buildsystem that can be used for Fedora/RHEL Modular packages, based on [Koji](https://pagure.io/koji/) and [Module Build Service](https://pagure.io/fm-orchestrator/).

The intention is for it to be trivially simple to get started with both, but also allow the same setup to be used for a production setup.

Full documentation can be found at: https://mbbox-operator.readthedocs.io/en/latest/

## Development environment
This project uses vagrant as development environment. To use the vagrant you need to have installed [`vagrant`](https://www.vagrantup.com/), [`vagrant_sshfs`](https://github.com/dustymabe/vagrant-sshfs) and [`libvirt`](https://libvirt.org/).

### Operator SDK vagrant box
To setup the development environment run `vagrant up` in root folder.

To recreate the environment run `vagrant destroy && vagrant up`. `vagrant provision` will not work in most cases because of the various OpenShift commands ran by the ansible provisioning script.

To enter the running vagrant box use `vagrant ssh`.

The box is set to use `docker` with [quay.io](https://quay.io) registry. For this to work properly you need to login to your quay.io account using `docker login quay.io`.

Follow MOTD (Message Of The Day) for more information.
