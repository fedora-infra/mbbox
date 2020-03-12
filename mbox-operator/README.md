# MBOX Operator

An ansible kubernetes operator for MBOX (Module Building in a Box).

Upstream ansible kubernetes operator docs: https://github.com/operator-framework/operator-sdk/tree/master/doc/ansible

## Usage

All commands work with `oc` as well.

Operator deployment and CRD creation (crds need to be create before deploying the operator):

```
kubectl apply -f deploy/crds/deploy/crds/apps.fedoraproject.org_mboxes_crd.yaml
kubectl apply -f deploy/
```

Checking if the operator is successfully running:

```
$ kubectl get pods -w
NAME                              READY   STATUS    RESTARTS   AGE
mbox-operator-6867d56dd4-q2ddq   2/2     Running   0          11m
```

Creating a mbox resource:

```
kubectl apply -f deploy/crds/apps.fedoraproject.org_v1alpha1_mbox_cr.yaml
```

## Development

Upstream user and development guide: https://github.com/operator-framework/operator-sdk/blob/master/doc/ansible/user-guide.md

## Testing

The operator sdk provides a `test`  subcommand which runs E2E tests against a cluster using the molecule cli.

It will run all tests added in the molecule folder, new tests have to added in molecule (`default/asserts.yml`) if changes were made in the operator itself.

More information on E2E testing can be found in the upstream documentation: https://github.com/operator-framework/operator-sdk/blob/master/doc/ansible/dev/testing_guide.md
