# mbox
Module Building in a Box

This repository contains a set of scripts used to set up a buildsystem that can be used for Fedora/RHEL Modular packages, based on [Koji](https://pagure.io/koji/) and [Module Build Service](https://pagure.io/fm-orchestrator/).

The intention is for it to be trivially simple to get started with both, but also allow the same setup to be used for a production setup.

## Usage

### Prerequisites
To use this tool, first make sure the `oc` command works, and you have a project in the openshift instance that you can use.

### Configuration
Then, copy `example.yml` to a configuration file of your choosing, and modify it.

Option | Description
-------|------------
`project_name` | The name of the Openshift Project to be used for deployment.
`template_dir` | The location (relative or absolute) of the "components" folder in the mbox repo.
`state_dir` | The location (relative or absolute) where the mbox state should be stored.
`ca.built_in` | Whether to use the built-in certificate authority. If disabled, you are expected to create certificates manually. Valid options: `yes`, `no`.
`ca.directory` | Used with `ca.built_in` set to `no`, to find where the certificates should be searched for.
`database.built_in` | Which Postgres template to use from Openshift. Valid options: `persistent`, `ephemeral` (warning: `ephemeral` means all database contents will be gone on every pod restart - this is not recommended except for testing)
`store.mnt_koji_volname` | If specified, `mnt_koji` (persistent storage for koji) will request this volume name. If left blank, Openshift will assign a random valid PersistentVolume.
`store.persistent_storage` | Whether to use persistent volume for koji. Possible values: `yes`, `no`. Use `no` only for testing or debugging purposes.
`koji_hub.public_hostname` | The hostname to be used for the Koji hub. Needs to be pointed at the Openshift router nodes.
`koji_hub.admin_username` | The username used for the Koji admin user.
`kojira.username` | The username used for Kojira (General maintenance tasks in Koji).
`builder.built_in` | Whether to deploy a builder into Openshift. Possible values: `yes`, `no`.
`identity.built_in` | Whether to deploy an OpenID Connect identity provider into the Openshift project. Valid options: `yes`. (Using an external identity provider is an outstanding task, contributions welcome).
`identity.public_hostname` | The hostname used for the built-in identity provider. Needs to be pointed at the Openshift router nodes.
`identity.etc_ipsilon_volname` | The Openshift Persistent Volume to use for the identity provider temporary storage. Can be left blank for auto-assigned Persistent Volume.
`mbs.public_hostname` | The hostname used for the Module Build Service deployment. Needs to be pointed at the Openshift router nodes.


### Running
After preparing and configuring, run `main.py`. The only required argument is the path to the configuration file.
Example: `./main.py mysetup.yml`.
After this, the deployment may take a few minutes.
This should result in a fully set up Koji and MBS setup, with one builder running inside Openshift, and a client certificate in the state directory.

### Connecting
The Koji instance should be available on the hostname configured as `koji_hub.public_hostname`.
You can use the client certificate named after `koji_hub.admin_username` to connect with the CLI, or run `./main.py configfile.py koji` and then the rest of the standard koji CLI options, and the koji CLI will be run preconfigured.

### Development environment
This project uses vagrant as development environment. There are two different vagrant boxes right now. One for testing and development of current script with OpenShift 3.11 and second for development of operator in OpenShift 4.x. To use the vagrant you need to have installed [`vagrant`](https://www.vagrantup.com/), [`vagrant_sshfs`](https://github.com/dustymabe/vagrant-sshfs) and [`libvirt`](https://libvirt.org/).

#### OpenShift 3.11 vagrant box
This will prepare the OpenShift 3.11 instance with mbox project in it. Box itself is named `mbbox_os311`. To setup the development run `vagrant up mbbox_os311` in root folder.

To recreate the environment run `vagrant destroy mbbox_os311 && vagrant up mbbox_os311`. `vagrant provision` will not work because of the various OpenShift commands ran by the ansible provisioning script.

To enter the running vagrant box use `vagrant ssh mbbox_os311`.

Follow MOTD for more information.

#### Operator SDK vagrant box
This will prepare vagrant box with Operator SDK and every prerequisite for it. Box itself is named `mbbox_osdk`. To setup the development run `vagrant up mbbox_osdk` in root folder.

To recreate the environment run `vagrant destroy mbbox_osdk && vagrant up mbbox_osdk`. `vagrant provision` will not work in most cases because of the various OpenShift commands ran by the ansible provisioning script.

To enter the running vagrant box use `vagrant ssh mbbox_osdk`.

The box is set to use `docker` with [quay.io](https://quay.io) registry. For this to work properly you need to login to your quay.io account using `docker login quay.io`.

Follow MOTD for more information.
