from .base import BaseComponent


class Kojira(BaseComponent):
    componentName = "kojira"
    deploymentConfigName = "kojira"

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="kojira",
        )
        self.state.apply_object_from_template(
            "kojira/buildconfig.yml",
        )
        return "kojira"

    def create(self):
        self.state.koji_hub.ensure_user("kojira")
        self.state.koji_hub.ensure_permission("kojira", "admin")
        self.state.ca.create_client_cert(
            "kojira",
        )
        self.state.apply_object_from_template(
            "kojira/configmap.yml",
            username=self.state.config.get("kojira", "username"),
        )
        self.state.apply_object_from_template(
            "kojira/deploymentconfig.yml",
        )
