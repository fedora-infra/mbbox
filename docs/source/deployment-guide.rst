================
Deployment Guide
================

This guide describes manual deployment process of MBBox operator in OpenShift 4 and Kubernetes Cluster.

Requirements
============

To be able to deploy MBBox operator manually you need to have admin rights to cluster. Otherwise you will not be able to deploy CRDs, roles, role bindings or service accounts.

To be able to deploy just the CR files you only need admin rights to namespace where you want to deploy operator.

Some commands require the usage of the "kustomize" CLI tool which an be found `here <https://kubectl.docs.kubernetes.io/installation/kustomize/binaries/>`_.

Makefile
========

We have a `Makefile <https://github.com/fedora-infra/mbbox/blob/master/mbox-operator/Makefile>`_ for you ready to be used. You just need to change a few things:

* `NS` variable must be set to namespace you are using (default value: default)

* In case `kubectl` is not available, you can use the same commands with `oc`

Prepare MBBox deployment
========================

To prepare cluster for MBBox deployment you just need to run following commands with the Makefile mentioned earlier in this guide.

.. code-block:: bash

   make install
   make deploy

This will apply CRDs files for MBBox and create roles, role bindings, service accounts and deploy the mbbox operator.

Create PVCs
===========
 
For deployment of the MBBox operator you need to prepare 2 PVCs. In case you are allowed to create PVCs this could be configured in CR files for koji-hub and mbox itself and they will be generated automatically based on the configuration. Otherwise you need to create them manually beforehand.

Most of the components are using Koji shared mount point. Check if the name of PVC is same in each component CR file otherwise the deployment will fail.

Prepare PostgreSQL DB
=====================

In case you have PostgreSQL DB running in cluster you can skip this step and just use the existing one.

To deploy PostgreSQL DB you can use the one `prepared by us <https://github.com/fedora-infra/mbbox/tree/master/components/psql>`__. You can change anything in those files, especially secret file. To deploy it run the following.

.. code-block:: bash

   kubectl apply -f components/psql -n <namespace>

Prepare RabbitMQ server
=======================

In case you have a running RabbitMQ server in your cluster, you can skip this step and just use the existing one.

To deploy RabbitMQ you can use the one `prepared by us <https://github.com/fedora-infra/mbbox/tree/master/components/rabbitmq>`__. You can change anything in those files, especially secret file. Refer to the `README.md` file for instructions about certificates. To deploy it run the following.

.. code-block:: bash

   kubectl apply -f components/rabbitmq -n <namespace>

.. note::
   Right now only Koji is emitting `Fedora messaging <https://fedora-messaging.readthedocs.io/en/stable/>`_ messages, which needs the RabbitMQ server.

CR Deployment
=============

Before deploying CR check the variables configuration. Please refer to :ref:`user-guide-label` for information about variables.

A full deployment needs to deploy a couple of CRs in order, `kustomize` can be used to achieve that:

.. code-block:: bash

   kustomize build config/samples | kubectl apply -f -

Delete Operator deployment
==========================

To delete operator deployment simply run:

.. code-block:: bash

   kustomize build config/samples | kubectl delete -f -
   make undeploy # This will delete the operator
   make uninstall # this will uninstall CRDs, roles, etc
