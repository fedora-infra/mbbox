from .base import BaseComponent


class MBSShared(BaseComponent):
    componentName = "MBS-shared"

    @property
    def is_inited(self):
        return self.state.oc_object_exists(
            "configmap",
            "mbs-configmap",
        )

    def create_build(self):
        self.logger.debug("Nothing to build")

    def create(self):
        self.state.database.ensure_database_exists("mbs")
        self.state.apply_object_from_template(
            "mbs_shared/configmap.yml",
            database_hostname=self.state.database.hostname,
            database_username=self.state.database.username,
            database_password=self.state.database.password,
            database_name='mbs',
        )
