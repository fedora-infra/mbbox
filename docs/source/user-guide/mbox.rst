============
mbox
============

This page documents the usage of mbox crd.

Description
===========

Mbox is a configuration resource that can be optionally used to defined shared configuration across other components.

Dependencies
============

`Mbox Custom Resource Definition (CRD) <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_mbox_crd.yaml>`_

Parameters
==========
    

+------------------------------+---------------------------------------------------+----------+
| Name                         | Default Value                                     | Type     |
+==============================+===================================================+==========+
| psql_secret_name             | postgres                                          |  string  |
+------------------------------+---------------------------------------------------+----------+
| koji_pvc_name                | mbox-koji-mnt                                     |  string  |
+------------------------------+---------------------------------------------------+----------+
| koji_pvc_size                | 10Gi                                              |  string  |
+------------------------------+---------------------------------------------------+----------+
| root_ca_secret_name          | mbox-koji-root-ca                                 |  string  |
+------------------------------+---------------------------------------------------+----------+
| koji_hub_host                | koji-hub:8443                                     |  string  |
+------------------------------+---------------------------------------------------+----------+
| mq_topic_prefix              | org.fedoraproject.dev                             |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs                          | {}                                                |  dict    |
+------------------------------+---------------------------------------------------+----------+
| mbs.scm_repo_url             | git+https://src.fedoraproject.org/modules/        |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs.rpm_repo_url             | git+https://src.fedoraproject.org/rpms/           |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs.pkg_repo_url            | https://src.fedoraproject.org/repo/pkgs/          |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs.pdc_url                  | https://pdc.stg.fedoraproject.org/rest_api/v1     |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs.backend_config_messaging | fedmsg                                            |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs.fedora_versions          | ['32']                                            | [string] |
+------------------------------+---------------------------------------------------+----------+
| mbs.topic_prefix             |  org.fedoraproject.dev                            |  string  |
+------------------------------+---------------------------------------------------+----------+
| mbs.configmap                |  mbs-configmap                                    |  string  |
+------------------------------+---------------------------------------------------+----------+


psql_secret_name
----------------

Postgresql secret used across many components to connect to a psql instance.

Deployment will fail if this secret is not present.

Secret format:

.. code-block:: yaml

  apiVersion: v1
  kind: Secret
  metadata:
    name: postgres
    labels:/
      app: postgres
  data:
    POSTGRES_HOST: fillme
    POSTGRES_DB: fillme
    POSTGRES_USER: fillme
    POSTGRES_PASSWORD: fillme

koji_pvc_name
-------------

The koji pvc name to be used as shared volume across components.

It will not create a PVC if one with the same name is already present.

koji_pvc_size
-------------

The koji pvc size to be used as shared volume across components.

This value will be ignore if using an existing volume instead of creating one.

root_ca_secret_name
-------------------

Root CA secret used to generate certificates across many components (koji clients, httpd, etc).

It will create a secret using self signed certs in case it does not exist.

.. code-block:: yaml

  apiVersion: v1
  kind: Secret
    metadata:
      name: mysecret
      namespace: default
      labels:
        app: mbox
    data:
      csr: -|
        fillme
      cert: -|
        fillme
      key: -|
        fillme 

koji_hub_host
-------------

The koji-hub internal service address (service name) and port to be used across koji and mbs components.

mq_topic_prefix
---------------

The MQ topic prefix to use when listening/emitting messages.

mbs
---

Shared config dictionary for both mbs frontend and backend.

This property is optional.

scm_repo_url
************

MBS scm repository git url to use.

This property is optional.

rpm_repo_url
************

MBS RPM repository git url.

This property is optional.

pkg_repo_url
************

MBS package repository url.

This property is optional.

pdc_url
*******

MBS PDC rest API url.

This property is optional.


backend_config_messaging
************************

Sets the mbs messaging system to use. We assume fedmsg as the default.

fedora_versions
***************

The versions of the Fedora we need to generate module template for.

oidc_required_scope
*******************

MBS OIDC required scope URL.

topic_prefix
***************

The MBS MQ topic prefix to use when listening/emitting messages.

configmap
*********

The MBS config map name to use when creating one.

It will skip its creation and an existing one if it already exists.

Usage
=====

Upstream file can be found `here <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_v1alpha1_mbox_cr.yaml>`_

Create a file containing the following content (modify as needed):

.. code-block:: yaml

  apiVersion: apps.fedoraproject.org/v1alpha1
  kind: Mbox
  metadata:
    name: example
  spec:
    psql_secret_name: postgres
    koji_pvc_name: mbox-koji-mnt
    koji_pvc_size: 10Gi
    root_ca_secret_name: mbox-koji-root-ca
    koji_hub_host: koji-hub:8443
    mq_topic_prefix: 'org.fedoraproject.dev'
    mbs:
      fedora_versions:
      - '32'
      scm_repo_url: 'git+https://src.fedoraproject.org/modules/'
      rpm_repo_url: 'git+https://src.fedoraproject.org/rpms/'
      pkg_repo_url: 'https://src.fedoraproject.org/repo/pkgs/'
      pdc_url: 'https://pdc.stg.fedoraproject.org/rest_api/v1'
      oidc_required_scope: 'https://mbs.fedoraproject.org/oidc/submit-build'
      config_system: koji
      backend_config_messaging: fedmsg
      hub_username: mbs

Run the following command to create a koji-builder resource:
  
.. code-block:: shell

  kubectl apply -f mbox-cr.yaml

You can check its status by running:

.. code-block:: shell

  kubectl get mbox/example -o yaml
