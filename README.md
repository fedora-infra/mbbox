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
`database.built_in` | Which Postgres template to use from Openshift. Valid options: `persistent`, `transient` (warning: `transient` means all database contents will be gone on every pod restart - this is not recommended except for testing)
`store.mnt_koji_volname` | If specified, `mnt_koji` (persistent storage for koji) will request this volume name. If left blank, Openshift will assign a random valid PersistentVolume.
`koji_hub.public_hostname` | The hostname to be used for the Koji hub. Needs to be pointed at the Openshift router nodes.
`koji_hub.admin_username` | The username used for the Koji admin user.
`kojira.username` | The username used for Kojira (General maintenance tasks in Koji).
`builder.built_in` | Whether to deploy a builder into Openshift. Possible values: `yes`, `no`.
`identity.built_in` | Whether to deploy an OpenID Connect identity provider into the Openshift project. Valud options: `yes`. (Using an external identity provider is an outstanding task, contributions welcome).
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
