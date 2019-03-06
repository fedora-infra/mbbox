from .base import BaseComponent


class MBSBackend(BaseComponent):
    componentName = "MBS-backend"
    deploymentConfigName = "mbs-backend"

    @property
    def backend_pod_name(self):
        return self.state.oc_get_object_name(
            "pod",
            "app=mbs-backend",
        )

    def run_command(self, *cmd):
        return self.state.oc_exec(
            self.backend_pod_name,
            *cmd,
        )

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="mbs-backend",
        )
        self.state.apply_object_from_template(
            "mbs_backend/buildconfig.yml",
        )
        return "mbs-backend"

    def create(self):
        self.state.koji_hub.ensure_user("mbs-backend")
        self.state.koji_hub.ensure_permission("mbs-backend", "admin")
        self.state.ca.create_client_cert(
            "mbs-backend",
        )
        self.state.apply_object_from_template(
            "mbs_backend/configmap.yml",
        )
        self.state.apply_object_from_template(
            "mbs_backend/deploymentconfig.yml",
            replicas=1,
        )
        self.state.oc_wait_for_deploy("mbs-backend")
        self.run_command(
            "/usr/bin/mbs-manager", "upgradedb",
        )
        for module in ("f29",):
            self.logger.info("Importing module %s", module)
            self.run_command(
                "/usr/bin/mbs-manager",
                "import_module",
                "/etc/module-build-service/default_module_%s.yml" % module,
            )
