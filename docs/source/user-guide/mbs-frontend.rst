============
mbs-frontend
============

This page documents the usage of mb-mbs-frontend crd.

Description
===========

The frontend of the module-build-service

Dependencies
============

`Mbox Module Build Service Frontend Custom Resource Definition (CRD) <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_mbmbsfrontends_crd.yaml>`_

Parameters
==========

+----------------------------+---------------------------------------------------+---------+
| Name                       | Default Value                                     | Type    |
+============================+===================================================+=========+
| replicas                   | 1                                                 | int     |
+----------------------------+---------------------------------------------------+---------+
| image                      | quay.io/fedora/mbs-frontend:latest                | string  |
+----------------------------+---------------------------------------------------+---------+
| configmap                  | mbs-frontend-configmap                            | string  |
+----------------------------+---------------------------------------------------+---------+
| https_enabled              | true                                              | boolean |
+----------------------------+---------------------------------------------------+---------+
| mbs_configmap              | mbs-configmap                                     | string  |
+----------------------------+---------------------------------------------------+---------+
| fedora_versions            | ['32']                                            |[string] |
+----------------------------+---------------------------------------------------+---------+
| hub_host                   | 'https://koji-hub:8443'                           | string  |
+----------------------------+---------------------------------------------------+---------+
| messaging_system           | 'fedmsg'                                          | string  |
+----------------------------+---------------------------------------------------+---------+
| topic_prefix               | 'org.fedoraproject.dev'                           | string  |
+----------------------------+---------------------------------------------------+---------+
| scm_url                    | 'git+https://src.fedoraproject.org/modules/'      | string  |
+----------------------------+---------------------------------------------------+---------+
| rpms_default_repository    | 'git+https://src.fedoraproject.org/rpms/'         | string  |
+----------------------------+---------------------------------------------------+---------+
| rpms_default_cache         | 'https://src.fedoraproject.org/repo/pkgs/'        | string  |
+----------------------------+---------------------------------------------------+---------+
| modules_default_repository | 'git+https://src.fedoraproject.org/modules/'      | string  |
+----------------------------+---------------------------------------------------+---------+
| postgres_secret            | postgres                                          | string  |
+----------------------------+---------------------------------------------------+---------+
| pdc_url                    | 'https://pdc.stg.fedoraproject.org/rest_api/v1'   | string  |
+----------------------------+---------------------------------------------------+---------+
| oidc_required_scope        | 'https://mbs.fedoraproject.org/oidc/submit-build' | string  |
+----------------------------+---------------------------------------------------+---------+
| ca_cert_secret             | koji-hub-ca-cert                                  | string  |
+----------------------------+---------------------------------------------------+---------+
| koji_hub_host              | 'koji-hub:8443'                                   | string  |
+----------------------------+---------------------------------------------------+---------+
| host                       | 'mbs.mbox.dev'                                    | string  |
+----------------------------+---------------------------------------------------+---------+
| client_cert_secret         | mbs-frontend-client-cert                          | string  |
+----------------------------+---------------------------------------------------+---------+
| service_cert_secret        | mbs-frontend-service-cert                         | string  |
+----------------------------+---------------------------------------------------+---------+


image
-----

The full qualified image name to pull mbs-frontend from.

replicas
--------

The amount of mbs-frontend replicas to deploy.

configmap
---------

The configmap name to use when deploying mbs-frontend

This configmap object contains mbs-frontend specific configuration files that are mounted in mbs-frontend pod filesystem.

https_enabled
-------------

A boolean flag that enables/disables https connections. If set to false http will be enabled.

mbs_configmap
-------------

The configmap name to use when deploying configuration shared between mbs-frontend and mbs-backend component.

This configmap contains configuration files that are shared between mbs-frontend and mbs-backend.

fedora_versions
---------------

The versions of the Fedora we need to generate module template for. 

hub_host
--------

The url of the running koji-hub instance.

messaging_system
----------------

Messaging system to use when sending messages. Support for fedora messaging is not available in MBS for now.

topic_prefix
------------

Prefix of the topic for messaging system.

config_scm_url
--------------

Source Code Management git URL for modules, should contain repositories for modules builds definitions.

rpms_default_repository
-----------------------

Default repository git URL for RPMS.

rpms_default_cache
------------------

Default cache URL for RPMS.

modules_default_repository
--------------------------

Default repository git URL for modules.

postgres_secret
---------------

Postgresql secret used by mbs-frontend to connect to a psql instance.

Depoyment will fail if this secret is not present.

Secret format:

.. code-block:: yaml

  apiVersion: v1
  kind: Secret
  metadata:
    name: postgres
    labels:
      app: postgres
  data:
    POSTGRES_HOST: fillme
    POSTGRES_DB: fillme
    POSTGRES_USER: fillme
    POSTGRES_PASSWORD: fillme

pdc_url
-------

Product Definition Center URL.

oidc_required_scope
-------------------

OIDC required scope URL.

ca_cert_secret
--------------

The root CA secret name to use.

If not provided it uses the one generated (self-signed).

koji_hub_host
-------------

Koji hub service name:port. This is used as common name for client certificate.

host
----

Hostname for MBS server. This is used as common name for server certificate.

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

service_cert_secret
-------------------

The httpd service secret name to use or create.

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
      app: koji-hub
  type: kubernetes.io/tls
  data:
    tls.crt: -|
      fillme
    tls.key: -|
      fillme

Usage
=====

Upstream file can be found `here <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_v1alpha1_mbmbsfrontend_cr.yaml>`_

Create a file mbmbsfrontend-cr.yaml containing the following content (modify as needed):

.. code-block:: yaml

apiVersion: apps.fedoraproject.org/v1alpha1
kind: MBMbsFrontend
metadata:
  name: mb-mbs-frontend
  labels:
    app: mb-mbs-frontend
spec:
  configmap: mbs-frontend-configmap
  https_enabled: true
  mbs_configmap: mbs-configmap
  fedora-versions: ['32']
  hub_host: 'https://koji-hub:8443'
  messaging_system: 'fedmsg'
  topic_prefix: 'org.fedoraproject.dev'
  scm_url: 'git+https://src.fedoraproject.org/modules/'
  rpms_default_repository: 'git+https://src.fedoraproject.org/rpms/' 
  rpms_default_cache: 'https://src.fedoraproject.org/repo/pkgs/'
  modules_default_repository: 'git+https://src.fedoraproject.org/modules/'
  postgres_secret: postgres
  pdc_url: 'https://pdc.stg.fedoraproject.org/rest_api/v1'
  oidc_required_scope: 'https://mbs.fedoraproject.org/oidc/submit-build'
  ca_cert_secret: koji-hub-ca-cert
  koji_hub_host: 'koji-hub:8443'
  host: 'mbs.mbox.dev'
  client_cert_secret: mbs-frontend-client-cert 
  service_cert_secret: mbs-frontend-service-cert

Run the following command to create a mbs-frontend resource:
  
.. code-block:: shell

  kubectl apply -f mbmbsfrontend-cr.yaml

You can check its status by running:

.. code-block:: shell

  kubectl get mbmbsfrontend/example -o yaml
