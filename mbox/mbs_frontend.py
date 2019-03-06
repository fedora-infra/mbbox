from .base import BaseComponent


class MBSFrontend(BaseComponent):
    componentName = "MBS-frontend"
    serviceName = "mbs-frontend"

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="mbs-frontend",
        )
        self.state.apply_object_from_template(
            "mbs_frontend/buildconfig.yml",
        )
        return "mbs-frontend"

    def create(self):
        self.state.ca.create_service_cert(
            "mbs-frontend",
            self.state.config.get("mbs", "public_hostname"),
        )
        self.state.apply_object_from_template(
            "mbs_frontend/configmap.yml",
        )
        self.state.apply_object_from_template(
            "mbs_frontend/deploymentconfig.yml",
            replicas=1,
        )
        self.state.apply_object_from_template(
            "mbs_frontend/service.yml",
        )
        self.state.apply_object_from_template(
            "mbs_frontend/route.yml",
            hostname=self.state.config.get('mbs', 'public_hostname'),
        )
        self.state.oc_wait_for_deploy("mbs-frontend")
