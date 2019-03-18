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
        username = self.state.config.get("kojira", "username")
        self.state.koji_hub.ensure_user(username)
        self.state.koji_hub.ensure_permission(username, "admin")
        self.state.ca.create_client_cert(
            "kojira",
        )
        self.state.apply_object_from_template(
            "kojira/configmap.yml",
            username=username,
        )
        self.state.apply_object_from_template(
            "kojira/deploymentconfig.yml",
        )
