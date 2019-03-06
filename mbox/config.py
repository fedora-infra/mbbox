import os.path
import yaml

from .base import BaseComponent


REQUIRED_KEYS = [
    'project_name',
    'template_dir',
    'state_dir',
    'database',
]


class Configuration(BaseComponent):
    componentName = "config"

    _loaded_config = None

    def create_build(self):
        self.logger.debug("Nothing to build")

    def ensure(self, *args, **kwargs):
        self.logger.debug("Config ensure is no-op")

    @property
    def _config(self):
        if self._loaded_config is None:
            with open(os.path.abspath(self.state._config_file), 'r') as f:
                self._loaded_config = yaml.safe_load(f)
        return self._loaded_config

    def validate(self):
        for key in REQUIRED_KEYS:
            if key not in self._config:
                raise ValueError("Required key %s not defined" % key)

        if not os.path.exists(self.template_dir):
            raise ValueError("Template directory does not exist")
        if not os.path.exists(self.state_dir):
            os.mkdir(self.state_dir)

    @property
    def project_name(self):
        return self._config['project_name']

    @property
    def template_dir(self):
        return os.path.abspath(self._config['template_dir'])

    @property
    def state_dir(self):
        return os.path.abspath(self._config['state_dir'])

    @property
    def database(self):
        return self._config['database']

    def get(self, object, key):
        return self._config[object][key]
