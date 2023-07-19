import os
import platform
import warnings
from typing import Any, Dict, Literal, Optional, Union

import yaml
from pydantic import BaseModel, BaseSettings, SecretStr

OS = platform.system()
if OS == "Darwin":
    _HOME_PATH = os.path.expanduser("~")
    DEFAULT_CONFIG_PATHS = [f"{_HOME_PATH}/.config/grai"]
elif OS == "Linux":
    _HOME_PATH = os.path.expanduser("~")
    DEFAULT_CONFIG_PATHS = [f"{_HOME_PATH}/.config/grai"]
elif OS == "Windows":
    _HOME_PATH = os.getenv("APPDATA")
    DEFAULT_CONFIG_PATHS = [f"{_HOME_PATH}/grai"]
elif OS == "":
    raise Exception("Python could not detect the type of your operating system. ")
else:
    warnings.warn(f"Operating system {OS} not recognized. Expected either 'Darwin', 'Windows', or 'Linux'")
    _HOME_PATH = os.path.expanduser("~")
    DEFAULT_CONFIG_PATHS = [f"{_HOME_PATH}/.config/grai"]

DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_PATHS[0]


class ConfigDirHandler:
    """ """

    DEFAULT_CONFIG_PATHS = DEFAULT_CONFIG_PATHS
    DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_PATHS[0]
    DEFAULT_CONFIG_FILE_NAMES = ["config.yaml", "config.yml"]

    def __init__(self):
        path = os.environ.get("GRAI_CLI_CONFIG_DIR", None)
        self.config_paths = [path, *self.DEFAULT_CONFIG_PATHS] if path is not None else [*self.DEFAULT_CONFIG_PATHS]
        self.default_config_file = os.path.join(self.DEFAULT_CONFIG_PATH, self.DEFAULT_CONFIG_FILE_NAMES[0])

        self.config_file: str = self.get_config_file()
        self.has_config_file: bool = self.config_file is not None
        self.config_dir: Optional[str] = os.path.dirname(self.config_file) if self.has_config_file else None

        self._config_content: Dict = None

    def get_config_file(self) -> Optional[str]:
        for path in self.config_paths:
            for filename in self.DEFAULT_CONFIG_FILE_NAMES:
                config_file = os.path.join(path, filename)
                if os.path.exists(config_file):
                    return config_file

        return None

    @property
    def config_content(self) -> Dict:
        """ """
        if isinstance(self._config_content, dict):
            return self._config_content
        elif not self.has_config_file:
            return {}

        with open(self.config_file, "r") as file:
            self._config_content = yaml.safe_load(file)
        return self._config_content

    @config_content.setter
    def config_content(self, value: Dict):
        """

        Args:
            value (Dict):

        Returns:

        Raises:

        """
        if not isinstance(value, dict):
            raise Exception("config_content must be a dictionary")
        self._config_content = value

    def save_content(self):
        """ """
        with open(self.config_file, "w") as file:
            yaml.safe_dump(self._config_content, file)


def unredact(obj: Any) -> Any:
    """

    Args:
        obj (Any):

    Returns:

    Raises:

    """
    if isinstance(obj, dict):
        return {k: unredact(v) for k, v in obj.items()}
    elif isinstance(obj, SecretStr):
        return obj.get_secret_value()
    else:
        return obj


config_handler = ConfigDirHandler()


def yaml_config_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """

    Args:
        settings:

    Returns:

    Raises:

    """
    return config_handler.config_content


class ServerSettingsV1(BaseModel):
    """ """

    api_version: Literal["v1"] = "v1"
    url: str
    workspace: str

    class Config:
        """ """

        validate_assignment = True


class AuthModeSettings(BaseModel):
    """ """

    authentication_mode: str

    class Config:
        """ """

        validate_assignment = True


class BasicAuthSettings(AuthModeSettings):
    """ """

    authentication_mode: Literal["username"] = "username"
    username: str
    password: SecretStr


class ApiKeySettings(AuthModeSettings):
    """ """

    authentication_mode: Literal["api_key"] = "api_key"
    api_key: SecretStr


class ContextSettings(BaseModel):
    """ """

    namespace: str = "default"


class GraiConfig(BaseSettings):
    """ """

    server: Union[ServerSettingsV1]
    auth: Union[BasicAuthSettings, ApiKeySettings]
    # context: Optional[ContextSettings]
    handler: ConfigDirHandler = config_handler

    def save(self):
        """ """
        values = unredact(self.dict(exclude={"handler"}))
        with open(self.handler.config_file, "w") as f:
            yaml.dump(values, f)

    def view(self):
        """ """
        return self.yaml(exclude={"handler"})

    @classmethod
    def default_config(cls):
        server = ServerSettingsV1(url="http://localhost:8000", workspace="default/default")
        auth = BasicAuthSettings(username="null@grai.io", password="super_secret")
        return cls(server=server, auth=auth)

    @classmethod
    def from_file(cls, file):
        with open(file, "r") as file:
            content = yaml.safe_load(file)

        return cls(**content)

    class Config:
        """ """

        env_prefix = "grai_"
        validate_assignment = True
        fields = {"server": {}, "auth": {"exclude": {"authentication_mode"}}, "context": {}}

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                yaml_config_settings_source,
            )


try:
    config = GraiConfig()

except Exception as e:
    message = (
        f"We were unable to construct a complete config file from provided environment variables and/or the config file "
        f"located at {config_handler.config_file}. This most likely means either \n"
        f"1) The config file is malformed, in which case you can edit it or execute `grai config init` to recreate it.\n"
        f"2) The config directory is incorrect. We've attempted looking in the following directories: "
        f"{config_handler.DEFAULT_CONFIG_PATHS} based on our operating system and the `GRAI_CLI_CONFIG_DIR` env var. \n"
        f"3) You may have made a mistake configuring your environment based purely on environment variables. \n"
        f"{os.environ.get('GRAI_CLI_CONFIG_DIR')}"
    )
    warnings.warn(message)
    config = GraiConfig.default_config()
