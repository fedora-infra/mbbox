from .base import BaseComponent


class Client(BaseComponent):
    componentName = "client"
    deploymentConfigName = "client"

    @property
    def client_pod_name(self):
        return self.state.oc_get_object_name(
            "pod",
            "app=client",
        )

    def run_command(self, *cmd, capture=False):
        return self.state.oc_exec(
            self.client_pod_name,
            *cmd,
            capture=capture,
        )

    def run_koji_command(self, *cmd, capture=False):
        return self.run_command(
            "koji", "--config=/etc/client/koji.conf",
            "--profile=koji",
            *cmd,
            capture=capture,
        )

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="client",
        )
        self.state.apply_object_from_template(
            "client/buildconfig.yml",
        )
        return "client"

    def create(self):
        self.state.ca.create_client_cert(
            "admin",
        )
        self.state.apply_object_from_template(
            "client/configmap.yml",
        )
        self.state.apply_object_from_template(
            "client/deploymentconfig.yml",
        )
        self.state.oc_wait_for_deploy("client")
