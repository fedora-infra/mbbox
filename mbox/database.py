import subprocess

from .base import BaseComponent


class Database(BaseComponent):
    componentName = "database"
    serviceName = "postgresql"

    _dbconn = None

    @property
    def db_pod_name(self):
        return self.state.oc_get_object_name(
            "pod",
            "name=postgresql",
        )

    @property
    def username(self):
        return "mboxdb"

    @property
    def password(self):
        return "mbox"

    @property
    def hostname(self):
        return "postgresql"

    def create_build(self):
        self.logger.debug("Nothing to do for build")

    def create(self):
        self.logger.debug("Creating database app")
        if not self.state.config.database['built_in'] in ('ephemeral',
                                                          'persistent'):
            raise ValueError("Invalid built-in db type")

        cmd = [
            "oc", "process",
            "-n", self.state.project_name,
            "openshift//postgresql-%s"
            % self.state.config.database['built_in'],
            "POSTGRESQL_USER=%s" % self.username,
            "POSTGRESQL_PASSWORD=%s" % self.password,
            "POSTGRESQL_DATABASE=mbox",
        ]
        objs = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            check=True,
        )
        self.state.oc_apply(objs.stdout)

    def run_query(self, database_name, query):
        self.logger.debug("Running database query on %s: %s",
                          database_name, query)
        return self.state.oc_exec(
            self.db_pod_name,
            """psql %s -c "%s" """ % (database_name, query)
        )

    def ensure_database_exists(self, database_name):
        self.logger.debug("Creating database %s", database_name)
        output = self.run_query(
            "mbox",
            "CREATE DATABASE %s OWNER mboxdb" % database_name,
        )
        if "already exists" in output.stderr:
            self.logger.debug("Database already existed")
            return False
        self.logger.debug("Stderr: %s" % output.stderr)
        output.check_returncode()
        self.logger.info("Database %s created", database_name)
        return True
