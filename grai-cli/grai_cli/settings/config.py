from functools import cache
import os
from confuse import LazyConfig, YamlSource, CONFIG_FILENAME
from grai_cli.settings.templates import get_config_parameters


def apply_redactions(config, redact_dict: dict):
    for path, value in redact_dict.items():
        view = config
        for key in path.split('.'):
            view = view[key]
        view.redact = value


class GraiLazyConfig(LazyConfig):
    def __init__(self, name, parameters, *args, **kwargs):
        super().__init__(name, __name__, *args, **kwargs)

        self.parameters = parameters
        self.set_args(self.parameters.default_values, dots=True)
        apply_redactions(self, self.parameters.redacted_fields)
        self.set_env()

    @property
    def config_filename(self):
        return os.path.join(self.config_dir(), CONFIG_FILENAME)


config = GraiLazyConfig('grai', get_config_parameters())
