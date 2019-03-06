from .base import BaseComponent


class KojiBuilder(BaseComponent):
    componentName = "koji_builder"
    deploymentConfigName = "koji-builder"

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="koji-builder",
        )
        self.state.apply_object_from_template(
            "koji_builder/buildconfig.yml",
        )
        return "koji-builder"

    def create(self):
        if not self.state.config.get('builder', 'built_in'):
            # Nothing to do yet
            # TODO: Maybe control certificates for external builders
            return
        self.state.koji_hub.ensure_builder_user(
            "koji-builder-built-in-1",
            "x86_64",
        )
        self.state.ca.create_client_cert(
            "koji-builder-built-in-1",
        )
        self.state.apply_object_from_template(
            "koji_builder/configmap.yml",
            maxjobs=5,
            vendor="MBox",
        )
        self.state.apply_object_from_template(
            "koji_builder/deploymentconfig.yml",
        )
