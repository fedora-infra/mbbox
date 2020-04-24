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
  operator-sdk test local #runs local tests as well, just a molecule cli wrapper

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
