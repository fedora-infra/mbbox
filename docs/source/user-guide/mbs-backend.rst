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

+----------------------------+---------------------------------------------------+---------+
| Name                       | Default Value                                     | Type    |
+============================+===================================================+=========+
| image                      | quay.io/fedora/mbs-backend:latest                 | string  |
+----------------------------+---------------------------------------------------+---------+
| replicas                   | 1                                                 | int     |
+----------------------------+---------------------------------------------------+---------+
| hub_username               | mbs                                               | string  |
+----------------------------+---------------------------------------------------+---------+
| cacert_secret              | mbs-ca-cert                                       | string  |
+----------------------------+---------------------------------------------------+---------+
| client_cert_secret         | mbs-client-cert                                   | string  |
+----------------------------+---------------------------------------------------+---------+
| postgres_secret            | postgres                                          | string  |
+----------------------------+---------------------------------------------------+---------+
| mbs_configmap              | mbs-configmap                                     | string  |
+----------------------------+---------------------------------------------------+---------+
| fedora_versions            | ['32']                                            |[string] |
+----------------------------+---------------------------------------------------+---------+
| hub_host                   | 'koji-hub:8443'                                   | string  |
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
| pdc_url                    | 'https://pdc.stg.fedoraproject.org/rest_api/v1'   | string  |
+----------------------------+---------------------------------------------------+---------+
| oidc_required_scope        | 'https://mbs.fedoraproject.org/oidc/submit-build' | string  |
+----------------------------+---------------------------------------------------+---------+
| shared_pvc                 | koji-hub-mnt-pvc                                  | string  |
+----------------------------+---------------------------------------------------+---------+
| mbox                       | ""                                                | string  |
+----------------------------+---------------------------------------------------+---------+


image
-----

The the full qualified image name to pull mbs-backend from.

replicas
--------

The amount of mbs-backend replicas to deploy.

hub_username
-------------

User to use when authenticating with koji-hub.

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

postgres_secret
---------------

Postgresql secret used by MBS to connect to a psql instance.

Deployment will fail if this secret is not present.

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

configmap
---------

The configmap name to use when deploying configuration shared between mbs-frontend and mbs-backend component.

This configmap contains configuration files that are shared between mbs-frontend and mbs-backend.

fedora_versions
---------------

The versions of the Fedora we need to generate module template for. 

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

pdc_url
-------

Product Definition Center URL.

oidc_required_scope
-------------------

OIDC required scope URL.

shared_pvc
----------

Name of the shared PersistentVolumeClaim mbs-backend will use.

mbox
----

A Mbox resource name to retrieve shared data from (pvc volume, shared certs and shared MBS configmap).

MBS Backend will use the following vars if this property is missing:

* shared_pvc (shared koji mnt volume)
* cacert_secret (root ca secret)
* postgres_secret (PSQL secret)
* configmap (shared configmap name) 
* fedora_versions (versions of fedora for module templates)
* hub_host (Koji host URL)
* messaging_system (messaging system to use)
* topic_prefix (topic prefix for messaging system)
* scm_url (URL for SCM)
* rpms_default_repository (default URL for RPMS repositories) 
* rpms_default_cache (default cache URL)
* modules_default_repository (default URL for modules repositories)
* pdc_url (URL for PDC)
* oidc_required_scope (OIDC required scope URL)

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
    replicas: 1
    image: quay.io/fedora/mbs-backend:latest
    hub_username: mbs
    cacert_secret: koji-hub-ca-cert
    client_cert_secret: mbs-client-cert
    postgres_secret: postgres
    configmap: mbs-configmap
    fedora_versions: ['32']
    hub_host: 'koji-hub:8443'
    messaging_system: 'fedmsg'
    topic_prefix: 'org.fedoraproject.dev'
    scm_url: 'git+https://src.fedoraproject.org/modules/'
    rpms_default_repository: 'git+https://src.fedoraproject.org/rpms/' 
    rpms_default_cache: 'https://src.fedoraproject.org/repo/pkgs/'
    modules_default_repository: 'git+https://src.fedoraproject.org/modules/'
    pdc_url: 'https://pdc.stg.fedoraproject.org/rest_api/v1'
    oidc_required_scope: 'https://mbs.fedoraproject.org/oidc/submit-build'
    shared_pvc: 'koji-hub-mnt-pvc'
    # mbox: example-mbox #uncomment to retrieve pvc and cert config from a mbox cr

Run the following command to create a mbs-backend resource:
  
.. code-block:: shell

  kubectl apply -f mbmbsbackend-cr.yaml

You can check its status by running:

.. code-block:: shell

  kubectl get mbmbsbackend/example -o yaml
