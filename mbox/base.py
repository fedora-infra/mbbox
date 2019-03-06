import logging


class BaseComponent(object):
    componentName = None
    serviceName = None
    deploymentConfigName = None
    buildName = None

    def __init__(self, state):
        if self.componentName is None:
            raise ValueError("No componentName configured")

        self.state = state
        self.logger = logging.getLogger(self.componentName)

    @property
    def is_inited(self):
        if self.serviceName is None and self.deploymentConfigName is None:
            raise ValueError("Component %s has no service or deploy name set"
                             % self.componentName)

        if self.serviceName:
            return self.state.oc_object_exists(
                "service",
                self.serviceName,
            )
        else:
            return self.state.oc_object_exists(
                "deploymentconfig",
                self.deploymentConfigName,
            )

    def ensure(self, force_update=False):
        if self.is_inited:
            self.logger.debug("Already inited")
            if force_update:
                self.logger.debug("Forcefully updating")
            else:
                return

        self.logger.debug("Creating")
        self.create()

    def create_build(self):
        raise NotImplementedError("Component %s missing create_build()"
                                  % self.componentName)

    def create(self):
        raise NotImplementedError("Component %s missing create()"
                                  % self.componentName)
