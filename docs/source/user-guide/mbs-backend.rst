============
mbs-backend
============

This page documents the usage of mb-mbs-backend crd.

Description
===========

The backend of the module-build-service

Dependencies
============

`Mbox Module Build Service Backend Custom Resource Definition (CRD) <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_mbmbsbackends_crd.yaml>`_

Parameters
==========

+-------------------------+-----------------------------------------------+---------+
| Name                    | Default Value                                 | Type    |
+=========================+===============================================+=========+
| image                   | quay.io/fedora/mbs-backend:latest             | string  |
+-------------------------+-----------------------------------------------+---------+
| replicas                | 1                                             | int     |
+-------------------------+-----------------------------------------------+---------+
| configmap               | mbs-backend-configmap                         | string  |
+-------------------------+-----------------------------------------------+---------+
| shared_pvc              | koji-hub-mnt-pvc                              | string  |
+-------------------------+-----------------------------------------------+---------+
| cacert_secret           | mbs-ca-cert                                   | string  |
+-------------------------+-----------------------------------------------+---------+
| client_cert_secret      | mbs-client-cert                               | string  |
+-------------------------+-----------------------------------------------+---------+
| hub_username            | mbs                                           | string  |
+-------------------------+-----------------------------------------------+---------+
| hub_url                 | 'https://koji-hub:8443'                       | string  |
+-------------------------+-----------------------------------------------+---------+
| consumer                | true                                          | string  |
+-------------------------+-----------------------------------------------+---------+
| poller                  | true                                          | string  |
+-------------------------+-----------------------------------------------+---------+
| config_system           | koji                                          | string  |
+-------------------------+-----------------------------------------------+---------+
| config_messaging        | fedmsg                                        | string  |
+-------------------------+-----------------------------------------------+---------+
| config_topic_prefix     | org.fedoraproject.dev                         | string  |
+-------------------------+-----------------------------------------------+---------+
| config_scm_url          | git+https://src.fedoraproject.org/modules/    | string  |
+-------------------------+-----------------------------------------------+---------+
| config_rpms_def_repo    | git+https://src.fedoraproject.org/rpms/       | string  |
+-------------------------+-----------------------------------------------+---------+
| config_rpms_def_cache   | https://src.fedoraproject.org/repo/pkgs/      | string  |
+-------------------------+-----------------------------------------------+---------+
| config_modules_def_repo | git+https://src.fedoraproject.org/modules/    | string  |
+-------------------------+-----------------------------------------------+---------+
| config_koji_repo_url    | https://kojipkgs.stg.fedoraproject.org/repos  | string  |
+-------------------------+-----------------------------------------------+---------+
| config_pdc_url          | https://pdc.stg.fedoraproject.org/rest_api/v1 | string  |
+-------------------------+-----------------------------------------------+---------+
| host_name               | koji-hub:8443                                 | string  |
+-------------------------+-----------------------------------------------+---------+
| ssl_verify              | true                                          | boolean |
+-------------------------+-----------------------------------------------+---------+
| fedora_versions         | ['32']                                        |[string] |
+-------------------------+-----------------------------------------------+---------+


image
-----

The the full qualified image name to pull mbs-backend from.

replicas
--------

The amount of mbs-backend replicas to deploy.

configmap
---------

The configmap name to use when deploying mbs-backend

This configmap object contains configuration files that are mounted in mbs-backend pod filesystem.

shared_pvc
----------

Shared PVC to be able to use the repository setup by koji-builder, defaults to koji-hub-mnt-pvc

cacert_secret
-------------

The root CA secret name to use.

If not provided it uses the one generated (self-signed).

client_cert_secret
------------------

The client secret name to use or create.

It will skip its creation (self signed) if one is already present.

It needs to be created and signed using the root CA certificate and private key.

Secret format:

.. code-block:: yaml

  apiVersion: v1
  kind: Secret
  metadata:
    name: myservice
    namespace: default
    labels:
      app: koji-builder
  type: kubernetes.io/tls
  data:
    tls.crt: -|
      fillme
    tls.key: -|
      fillme
    tls.pem: -|
      This is a combination of tls.key and tls.crt separated by '\n' and encoded in base64
      Example: "{{ (lookup('file', 'client_key.pem') + '\n' + lookup('file', 'client_cert.pem')) | b64encode }}"

hub_username
-------------

User to use when authenticating with koji-hub.

hub_url
-------

Location of the koji-hub to connect to.

consumer
--------

Sets up to consume messages through fedmsg.

poller
------

Sets up a poller to watch for the status of module builds.

config_system
-------------

Configures the buildsystem to use. We assume koji as the default.

config_messaging
----------------

Configures the messaging system to use. We assume fedmsg as the default.

config_topic_prefix
-------------------

Configures the topic prefix for the messages we are interested in.


config_scm_url
--------------

Configures the scm containing the module definitions

config_rpms_def_repo
--------------------

Configures the scm containing the srpm definitions


config_rpms_def_cache
---------------------

Configures the scm containing the package cache


config_modules_def_repo
-----------------------

Configures the scm containing the module definitions


config_koji_repo_url
--------------

Configures the koji rpm repository

config_pdc_url
--------------

Configures the URL for the Product Definition Centre

fedora_versions
--------------

The versions for the Fedora 32 

Usage
=====

Upstream file can be found `here <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_v1alpha1_mbmbsbackend_cr.yaml>`_

Create a file mbmbsbackend-cr.yaml containing the following content (modify as needed):

.. code-block:: yaml

apiVersion: apps.fedoraproject.org/v1alpha1
kind: MBMbsBackend
metadata:
  name: example-mb-mbs-backend
spec:
  hub_username: mbs
  hub_url: "https://koji:8443"
  cacert_secret: koji-hub-ca-cert
  client_cert_secret: mbs-client-cert
  configmap: mbs-backend-configmap
  postgres_secret: postgres
  consumer: true
  poller: true
  fedora_versions: ['32']
  config_system: 'koji'
  config_messaging: 'fedmsg'
  config_topic_prefix: 'org.fedoraproject.dev'
  config_scm_url: 'git+https://src.fedoraproject.org/modules/'
  config_rpms_def_repo: 'git+https://src.fedoraproject.org/rpms/'
  config_rpms_def_cache: 'https://src.fedoraproject.org/repo/pkgs/'
  config_modules_def_repo: 'git+https://src.fedoraproject.org/modules/'
  config_koji_repo_url: 'https://kojipkgs.stg.fedoraproject.org/repos'
  config_pdc_url: 'https://pdc.stg.fedoraproject.org/rest_api/v1'

Run the following command to create a mbs-backend resource:
  
.. code-block:: shell

  kubectl apply -f mbmbsbackend-cr.yaml

You can check its status by running:

.. code-block:: shell

  kubectl get mbmbsbackend/example -o yaml
