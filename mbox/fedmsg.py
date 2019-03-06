from .base import BaseComponent


class FedmsgComponent(BaseComponent):
    componentName = "fedmsg-relay"
    serviceName = "fedmsg-relay"

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="fedmsg-relay",
        )
        self.state.apply_object_from_template(
            "fedmsg/buildconfig_relay.yml",
        )
        return "fedmsg-relay"

    def create(self):
        self.state.apply_object_from_template(
            "general/fedmsgd.yml",
        )
        self.state.apply_object_from_template(
            "fedmsg/deploymentconfig_relay.yml",
        )
        self.state.apply_object_from_template(
            "fedmsg/service_relay.yml",
        )
        self.state.oc_wait_for_deploy("fedmsg-relay")
