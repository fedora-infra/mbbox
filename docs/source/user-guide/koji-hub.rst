========
koji-hub
========

This page documents the usage of koji-hub crd.

Dependencies
============

`Koji-Hub Custom Resource Definition (CRD) <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_mbkojihubs_crd.yaml>`_

Koji-hub depends the following external components:

* postgresql
* fedora messaging

The operator does not deploy those components and it expects those to be are already available/deployed.

Sample deployment files are provided for development/example purposes:

* `postgresql <https://github.com/fedora-infra/mbbox/tree/master/components/psql>`_
* `rabbitmq <https://github.com/fedora-infra/mbbox/tree/master/components/rabbitmq>`_

Parameters
==========

+------------------------+--------------------------------+---------+
| Name                   | Default Value                  | Type    |
+========================+================================+=========+
| image                  | quay.io/fedora/koji-hub:latest | string  |
+------------------------+--------------------------------+---------+
| replicas               | 1                              | int     |
+------------------------+--------------------------------+---------+
| persistent             | true                           | boolean |
+------------------------+--------------------------------+---------+
| host                   | koji-hub                       | string  |
+------------------------+--------------------------------+---------+
| configmap              | koji-hub                       | string  |
+------------------------+--------------------------------+---------+
| ca_cert_secret         | koji-hub-ca-cert               | string  |
+------------------------+--------------------------------+---------+
| service_cert_secret    | koji-hub-service-cert          | string  |
+------------------------+--------------------------------+---------+
| postgres_secret        | postgres                       | string  |
+------------------------+--------------------------------+---------+
| http_enabled           | true                           | boolean |
+------------------------+--------------------------------+---------+
| https_enabled          | true                           | boolean |
+------------------------+--------------------------------+---------+
| topic_prefix           | mbox_dev                       | string  |
+------------------------+--------------------------------+---------+
| fedora_messaging_url   |                                | string  |
+------------------------+--------------------------------+---------+
| messaging_cert_cm      | koji-hub-msg                   | string  |
+------------------------+--------------------------------+---------+
| ingress_backend        | nginx                          | string  |
+------------------------+--------------------------------+---------+
| mbox                   | ""                             | string  |
+------------------------+--------------------------------+---------+
| httpd_pvc_name         | koji-hub-httpd-pvc             | string  |
+------------------------+--------------------------------+---------+
| httpd_pvc_size         | 1Gi                            | string  |
+------------------------+--------------------------------+---------+
| mnt_pvc_name           | koji-hub-mnt-pvc               | string  |
+------------------------+--------------------------------+---------+
| mnt_pvc_size           | 10Gi                           | string  |
+------------------------+--------------------------------+---------+
| web_client_cert_secret | koji-hub-web-client-cert       | string  |
+------------------------+--------------------------------+---------+
| web_client_username    | kojihub                        | string  |
+------------------------+--------------------------------+---------+


image
-----

The the full qualified image name to pull koji-hub from.

replicas
--------

The amount of koji-hub replicas to deploy.

persistent
----------

A boolean flag to enable/disable pvc creation.

Note: I will not create any external volumes if set to false.

host
----

The koji-hub hostname to be used on several config files and certificates such as httpd.

This property should be set to the public base url of koji on production environments.

configmap
---------

The configmap name to use when deploying koji-hub.

This configmap object contains configuration files that are mounted in koji-hub pod filesystem.

ca_cert_secret
--------------

The root CA secret name to use or create.

It will skip its creation (self signed) if one is already present.

Secret format:

.. code-block:: yaml

  apiVersion: v1
  kind: Secret
    metadata:
      name: mysecret
      namespace: default
      labels:
        app: koji-hub
    data:
      csr: -|
        fillme
      cert: -|
        fillme
      key: -|
        fillme

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

postgres_secret
---------------

Postgresql secret used by koji-hub to connect to a psql instance.

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

http_enabled
------------

A boolean flag that enables/disables http connections.

https_enabled
-------------

A boolean flag that enables/disables https connections.

topic_prefix
------------

The fedora messaging topic prefix to use koji-hub config.

fedora_messaging_url
--------------------

The fedora messaging url to use in koji-hub.

This is a required property with no default value.

messaging_cert_cm
-----------------

A config map that contains fedora messaging certs to be mounted in koji-hub pod filesystem.

Those files are used to authenticate koji-hub to a fedora-messaging instance.

Config map format:

.. code-block:: yaml

  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: koji-hub-msg
    namespace: default
    labels:
      app: koji-hub
  data:
    koji.ca: |-
      fillme
    koji.crt: |-
      fillme
    koji.key: |-
      fillme


ingress_backend
---------------

The kubernetes ingress backend to use when creating an ingress resource for koji-hub.

Available choices:

* nginx

httpd_pvc_name
--------------

Name of the PersistentVolumeClaim for httpd server koji-hub will use.

If provided PVC doesn't exists, it creates its own.

httpd_pvc_size
--------------

Size of the PersistentVolumeClaim for httpd server koji-hub will create.

If httpd_pvc_name exists, this value is ignored.

mnt_pvc_name
------------

Name of the PersistentVolumeClaim koji-hub will use.

If provided PVC doesn't exists, it creates its own.

mnt_pvc_size
------------

Size of the PersistentVolumeClaim koji-hub will create.

If mnt_pvc_name exists, this value is ignored.

mbox
----

A Mbox resource name to retrieve shared data from (pvc volume and shared certs).

Koji-builder will use the following vars if this property is missing to create/use those shared resources:

* mnt_pvc_name (shared koji mnt volume)
* ca_cert_secret (root ca secret)
* postgres_secret (PSQL secret)

web_client_cert_secret
----------------------

The koji-web secret name to use or create for koji-hub authentication.

It will skip its creation (self signed) if one is already present.

It needs to be created and signed using the root CA certificate and private key.

It should have one key "client.pem" to store both private key and public certificate.

The certificate's CN field will be used as username during authentication. 

Secret format:

.. code-block:: yaml

  apiVersion: v1
  kind: Secret
  metadata:
    name: koji-hub-wen-client-cert-secret
    namespace: default
    labels:
      app: koji-hub
  data:
    client.pem: -|
      fillme


web_client_username
-------------------

Koji web client username to be used when authenticating to koji-hub.

This property will be ignored if not using a self-signed certificate generated by the operator.


Usage
=====

Upstream file can be found `here <https://raw.githubusercontent.com/fedora-infra/mbbox/master/mbox-operator/deploy/crds/apps.fedoraproject.org_v1alpha1_mbkojihub_cr.yaml>`_

Create a file containing the following content (modify as needed):

.. code-block:: yaml

  apiVersion: apps.fedoraproject.org/v1alpha1
  kind: MBKojiHub
  metadata:
    name: example
    labels:
      app: mbox
  spec:
    image: quay.io/fedora/koji-hub:latest
    replicas: 1
    persistent: true
    host: koji-hub
    configmap: koji-hub
    ca_cert_secret: koji-hub-ca-cert
    service_cert_secret: koji-hub-service-cert
    postgres_secret: postgres
    http_enabled: true
    https_enabled: true
    topic_prefix: mbox_dev
    fedora_messaging_url: amqps://koji@messaging.url
    messaging_cert_cm: koji-hub-msg
    ingress_backend: nginx

Run the following command to create a koji-hub resource:
  
.. code-block:: shell

  kubectl apply -f koji-hub-cr.yaml

You can check its status by running:

.. code-block:: shell

  kubectl get mbkojihub/example -o yaml
