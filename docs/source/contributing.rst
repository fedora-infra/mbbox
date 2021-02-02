============
Contributing
============

Mbox welcomes contributions! Our issue tracker is located on `GitHub <https://github.com/fedora-infra/mbbox/issues>`_.

Guidelines
===========

When you make a pull request, someone from the fedora organization
will review your code. Please make sure you follow the guidelines below:

Code Style
----------

Make sure your yaml code passes our yamllint rules.

E2E Tests
---------

Every change should be tested in molecule, which is the tool we use for E2E (end to end) testing.

Tests can be run using either molecule or operator-sdk cli (which uses molecule as well).

.. code-block:: bash

  molecule test -s test-local #local tests, no need for a cluster
  molecule test -s test-cluster #needs a remote cluster, minikube is enough

Debugging Local Tests
---------------------

If you encounter any error when running test you can debug the issue by connecting to local instance of kubernetes running in docker:

.. code-block:: bash

   molecule converge -s test-local #runs local test without destroy sequence
   docker ps #find container named kind-test-local
   docker exec -it <container_id> bash #<container_id> of container from previous command
   kubectl config set-context --current --namespace=osdk-test #sets namespace to operator-sdk

Here are few useful commands for debugging, for another commands look at `kubectl help`:

.. code-block:: bash

   kubectl get all #returns all resources in the current namespace
   kubectl logs <pod> #shows logs for specific <pod>
   kubectl logs <mbox-operator-pod> ansible #shows ansible logs for <mbox-operator-pod>
   kubectl describe <resource> #shows detailed information about specific <resource>
   kubectl get ingress #returns all ingress resources, is not part of get all

Troubleshooting
---------------

During the development, we encountered some issues when debugging operator deployment. We will try to document them in this section, together with solutions.

Issue: Timeout in reconciliation task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This was caused by low space, because failing tests aren't removing docker volumes when they fails. To remove the volumes run following command `docker volume prune`.

Issue: Can't reach service from the pod in minikube
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This issue is caused by network problem inside docker running minikube cluster. You can encounter this issue in vagrant when trying to access the service from pod which
is linked to the service.

To fix this just run the following:

.. code-block:: bash

   minikube ssh
   sudo ip link set docker0 promisc on

Environment
===========

We are providing a full development environment in Vagrant but you can use your host machine as long as you meet the following requirements:

* ansible >= 2.9
* molecule >= 3
* yamllint >= 1.20
* python kubernetes and openshift libraries
* operator-sdk >= 0.16
* docker >= 19

NOTE: make sure both ansible and molecule are system-wide installed using in the same python interpreter otherwise you may have issues running tests.

Setting Up Vagrant Environment
------------------------------

To start the vagrant operator SDK box, run the following in project root:

.. code-block:: bash

   vagrant up #starts the vagrant VM, it could take a while
   vagrant reload #this is needed to remount the sshfs mounts after reboot when cgroups are changed to V1
   vagrant ssh #connects you to the vagrant VM

In vagrant VM you can find project folder in `~/devel`.
To run the tests do `cd ~/devel/mbox-operator` and follow `E2E Tests`_ section.

If you encounter any issue with `vagrant up` command, do `vagrant destroy` to be sure that there isn't any leftover from previous run.
