from confuse import MappingValues, OneOf


class ConfigParameters:
    def __init__(self, template, default_values, redacted_fields):
        self.template = template
        self.default_values = default_values
        self.redacted_fields = redacted_fields


def _get_config_template():
    ##########################

    server_template = {
        "host": str,
        "port": int,
    }

    ##########################
    auth_user_template = {
        "user": str,
        "password": str,
    }

    auth_api_template = {
        "api_key": str,
    }

    auth_template = MappingValues(OneOf([auth_user_template, auth_api_template]))

    ###########################

    context_template = {
        "namespace": str
    }

    ###########################

    template = {
        "server": server_template,
        "auth": auth_template,
        "context": context_template,
    }
    return template


def get_config_parameters():
    default_values = {
        "server.host": "localhost",
        "server.port": "8000",
        "context.namespace": "default", 
    }

    redacted_fields = {
        'auth.password': True,
        'auth.api_key': True,
    }

    template = _get_config_template()

    return ConfigParameters(template, default_values, redacted_fields)


