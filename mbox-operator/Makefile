SHELL = /bin/bash
NS = default

.PHONY: prepare/crds
prepare/crds:
	@kubectl apply -f deploy/crds/apps.fedoraproject.org_mbkojihubs_crd.yaml
	@kubectl apply -f deploy/crds/apps.fedoraproject.org_mboxes_crd.yaml

.PHONY: prepare/rbac
prepare/rbac:
	@kubectl apply -f deploy/role.yaml -n ${NS}
	@kubectl apply -f deploy/role_binding.yaml -n ${NS}
	@kubectl apply -f deploy/service_account.yaml -n ${NS}

.PHONY: prepare
prepare: prepare/crds prepare/rbac

.PHONY: prepare/crs
prepare/crs:
	@kubectl apply -f deploy/crds/apps.fedoraproject.org_v1alpha1_mbkojihub_cr.yaml -n ${NS} || true

.PHONY: deploy
deploy: prepare
	@kubectl apply -f deploy/operator.yaml -n ${NS}

.PHONY: delete/crds
delete/crds:
	@kubectl delete -f deploy/crds/apps.fedoraproject.org_mbkojihubs_crd.yaml || true
	@kubectl delete -f deploy/crds/apps.fedoraproject.org_mboxes_crd.yaml || true

.PHONY: delete/crs
delete/crs:
	@kubectl delete -f deploy/crds/apps.fedoraproject.org_v1alpha1_mbkojihub_cr.yaml -n ${NS} || true

.PHONY: delete/rbac
delete/rbac:
	@kubectl delete -f deploy/role.yaml -n ${NS} || true
	@kubectl delete -f deploy/role_binding.yaml -n ${NS} || true
	@kubectl delete -f deploy/cluster_role_binding.yaml || true
	@kubectl delete -f deploy/service_account.yaml -n ${NS} || true

.PHONY: delete
delete: delete/crds delete/rbac
	@kubectl delete -f deploy/operator.yaml -n ${NS} || true

.PHONY: run
run:
	kubectl apply -f deploy/crds/apps.fedoraproject.org_v1alpha1_mbkojihub_cr.yaml
