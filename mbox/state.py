import jinja2
import subprocess
import logging
import time

import mbox.ca
import mbox.config
import mbox.client
import mbox.database
import mbox.fedmsg
import mbox.identity
import mbox.koji_builder
import mbox.koji_hub
import mbox.kojira
import mbox.mbs_backend
import mbox.mbs_frontend
import mbox.mbs_shared


COMPONENT_CLASSES = {
    "ca": mbox.ca.CertificateAuthority,
    "config": mbox.config.Configuration,
    "client": mbox.client.Client,
    "database": mbox.database.Database,
    "fedmsg": mbox.fedmsg.FedmsgComponent,
    "identity": mbox.identity.Identity,
    "koji_builder": mbox.koji_builder.KojiBuilder,
    "koji_hub": mbox.koji_hub.KojiHub,
    "kojira": mbox.kojira.Kojira,
    "mbs_backend": mbox.mbs_backend.MBSBackend,
    "mbs_frontend": mbox.mbs_frontend.MBSFrontend,
    "mbs_shared": mbox.mbs_shared.MBSShared,
}
COMPONENT_ORDER = [
    "config",
    "ca",
    "fedmsg",
    "database",
    "koji_hub",
    "client",
    "koji_builder",
    "kojira",
    "identity",
    "mbs_shared",
    "mbs_backend",
    "mbs_frontend",
]


class State(object):
    # Settings
    _print_oc_output = None
    _config_file = None

    # Helpers
    _jinjaenv = None

    # Component instances
    _components = {}

    def __init__(self, config_file, print_oc_output):
        self.logger = logging.getLogger("state")
        self._config_file = config_file
        self._print_oc_output = print_oc_output

        self.config.validate()

    @property
    def project_name(self):
        return self.config.project_name

    @property
    def capture_oc_output(self):
        return not self._print_oc_output

    def oc_test(self):
        subprocess.run(["oc", "whoami"], capture_output=True, check=True)

    def oc_apply(self, obj):
        subprocess.run(
            ["oc", "apply", "-f", "-", "-n", self.project_name],
            input=obj,
            encoding='utf-8',
            check=True)

    @staticmethod
    def _objname(objtype, objname):
        return "%s/%s" % (objtype, objname)

    def oc_object_exists(self, objtype, objname):
        self.logger.debug("Checking if %s/%s exists", objtype, objname)
        res = subprocess.run(
            ["oc", "get", "-n", self.project_name,
             self._objname(objtype, objname)],
            capture_output=True)
        self.logger.debug("Exists: %s", res.returncode == 0)
        return res.returncode == 0

    def oc_create_secret_file(self, objname, files):
        """ Create a secret from a set of files.

        files: dict of key -> filename to upload.
        """
        self.logger.debug("Creating secret file %s", objname)
        cmd = ["oc", "-n", self.project_name,
               "create", "secret", "generic", objname]
        for file in files:
            cmd.append("--from-file=%s=%s" % (file, files[file]))
        subprocess.run(
            cmd,
            encoding='utf-8',
            check=True)

    def oc_create_secret_tls(self, objname, cert, key):
        self.logger.debug("Creating TLS secret %s", objname)
        cmd = ["oc", "-n", self.project_name,
               "create", "secret", "tls", objname,
               "--cert=%s" % cert,
               "--key=%s" % key]
        subprocess.run(
            cmd,
            encoding='utf-8',
            check=True)

    def oc_get_last_build_num(self, bcname):
        self.logger.debug("Getting last build for buildconfig %s", bcname)
        cmd = [
            "oc", "-n", self.project_name,
            "get", self._objname("buildconfig", bcname),
            "-o=custom-columns=LATEST:status.lastVersion",
            "--no-headers=true",
        ]
        res = subprocess.run(
            cmd,
            encoding='utf-8',
            check=True,
            capture_output=True,
        )
        return res.stdout.strip()

    def oc_ensure_build(self, buildname, follow=True):
        self.logger.debug("Ensuring build for %s", buildname)
        last = self.oc_get_last_build_num(buildname)
        if last is not '0':
            self.logger.debug("Build was already fired once: %s", last)
            return
        self.logger.debug("Starting build for %s", buildname)
        cmd = [
            "oc", "-n", self.project_name,
            "start-build", buildname,
        ]
        if follow:
            cmd += ['--follow=true']
        return subprocess.run(
            cmd,
            encoding='utf-8',
            check=True,
            capture_output=self.capture_oc_output,
        )

    def oc_wait_for_deploy(self, deployname):
        self.logger.debug("Waiting for deploy of %s", deployname)
        # oc rollout status dc/koji-hub -n mbox --watch
        cmd = [
            "oc", "-n", self.project_name,
            "rollout", "status", self._objname("deploymentconfig", deployname),
            "--watch=true",
        ]
        subprocess.run(
            cmd,
            encoding='utf-8',
            check=True,
            capture_output=self.capture_oc_output,
        )
        self.logger.debug("Waiting 5 seconds for deployment to be done")
        time.sleep(5)

    def oc_get_object_name(self, objtype, *filters):
        self.logger.debug("Getting object type %s filters %s",
                          objtype, filters)
        cmd = [
            "oc", "-n", self.project_name,
            "get", objtype, "-o", "name",
            "--show-all=false",
        ]
        for filter in filters:
            cmd.extend(["-l", filter])
        return subprocess.run(
            cmd,
            encoding='utf-8',
            check=True,
            capture_output=True,
        ).stdout.strip().split("\n")[-1].strip()

    def oc_exec(self, podname, *command):
        if podname.startswith('pod/'):
            podname = podname[len('pod/'):]
        if isinstance(command, tuple):
            command = list(command)
        if isinstance(command, list):
            command = " ".join(command)
        self.logger.debug("Running command in pod %s: %s", podname, command)
        cmd = [
            "oc", "-n", self.project_name,
            "exec", podname, "--",
            "/bin/bash", "-c",
            command,
        ]
        res = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            check=False,
        )
        self.logger.debug("Retcode: %d", res.returncode)
        self.logger.debug("Stdout: %s", res.stdout)
        self.logger.debug("Stderr: %s", res.stderr)
        return res

    @property
    def jinjaenv(self):
        if self._jinjaenv is None:
            self._jinjaenv = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.config.template_dir),
                autoescape=False,
            )
            self._jinjaenv.globals['project_name'] = self.project_name
        return self._jinjaenv

    def apply_object_from_template(self, template_path, **template_vars):
        templ = self.jinjaenv.get_template(template_path)
        obj = templ.render(**template_vars)
        self.oc_apply(obj)

    def get_component(self, component_name):
        if component_name not in self._components:
            component_class = COMPONENT_CLASSES[component_name]
            self.logger.debug("Initializing component %s, class: %s",
                              component_name,
                              component_class)
            self._components[component_name] = component_class(self)
        return self._components[component_name]

    def build_all(self):
        bcs = []
        for component in COMPONENT_ORDER:
            self.logger.info("Starting build for component %s", component)
            bcname = self.get_component(component).create_build()
            if bcname is not None:
                bcs.append(bcname)
                self.oc_ensure_build(bcname, follow=False)

    def ensure_all(self, forced=[]):
        for component in COMPONENT_ORDER:
            self.logger.info("Ensuring component %s", component)
            self.get_component(component).ensure(
                force_update=component in forced,
            )

    @property
    def ca(self):
        return self.get_component("ca")

    @property
    def config(self):
        return self.get_component("config")

    @property
    def client(self):
        return self.get_component("client")

    @property
    def database(self):
        return self.get_component("database")

    @property
    def fedmsg(self):
        return self.get_component("fedmsg")

    @property
    def identity(self):
        return self.get_component("identity")

    @property
    def koji_builder(self):
        return self.get_component("koji_builder")

    @property
    def koji_hub(self):
        return self.get_component("koji_hub")

    @property
    def mbs_backend(self):
        return self.get_component("mbs_backend")

    @property
    def mbs_frontend(self):
        return self.get_component("mbs_frontend")

    @property
    def mbs_shared(self):
        return self.get_component("mbs_shared")
