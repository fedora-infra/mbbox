from .base import BaseComponent


class Identity(BaseComponent):
    componentName = "identity"
    serviceName = "identity"

    def create_build(self):
        self.state.apply_object_from_template(
            "general/imagestream.yml",
            imagename="identity",
        )
        self.state.apply_object_from_template(
            "identity/buildconfig.yml",
        )
        return "identity"

    def create(self):
        if not self.state.config.get('identity', 'built_in'):
            # TODO: Nothing to do yet
            return
        self.state.ca.create_service_cert(
            "identity",
            self.state.config.get('identity', 'public_hostname'),
        )
        self.state.database.ensure_database_exists("ipsilon")
        self.state.apply_object_from_template(
            "identity/etcipsilon.yml",
            volumename=self.state.config.get('identity', 'etc_ipsilon_volname'),
        )
        self.state.apply_object_from_template(
            "identity/configmap.yml",
            database_username=self.state.database.username,
            database_password=self.state.database.password,
            database_hostname=self.state.database.hostname,
            database_name='ipsilon',
        )
        self.state.apply_object_from_template(
            "identity/deploymentconfig.yml",
            replicas=1,
        )
        self.state.apply_object_from_template(
            "identity/service.yml",
        )
        self.state.apply_object_from_template(
            "identity/route.yml",
            hostname=self.state.config.get('identity', 'public_hostname'),
        )
        self.state.oc_wait_for_deploy("identity")
