import os
import platform
import warnings
from typing import Any, Dict, Literal, Optional, Union

import yaml
from pydantic import BaseModel, BaseSettings, SecretStr
from pydantic_yaml import YamlModel, YamlModelMixin, YamlStrEnum


class ConfigDirHandler:
    """ """

    DEFAULT_CONFIG_FILE_NAMES = ["config.yaml", "config.yml"]

    def __init__(self):
        self.os = platform.system()
        if self.os == "Darwin":
            _HOME_PATH = os.path.expanduser("~")
            config_paths = [f"{_HOME_PATH}/.config/grai"]
        elif self.os == "Linux":
            _HOME_PATH = os.path.expanduser("~")
            config_paths = [f"{_HOME_PATH}/.config/grai"]
        elif self.os == "Windows":
            _HOME_PATH = os.getenv("APPDATA")
            config_paths = [f"{_HOME_PATH}/grai"]
        elif self.os == "":
            raise Exception("Python could not detect the type of your operating system. ")
        else:
            warnings.warn(f"Operating system {self.os} not recognized. Expected either 'Darwin', 'Windows', or 'Linux'")
            _HOME_PATH = os.path.expanduser("~")
            config_paths = [f"{_HOME_PATH}/.config/grai"]

        self.config_paths = config_paths
        self.default_config_path = self.config_paths[0]
        self.default_config_file = os.path.join(self.default_config_path, self.DEFAULT_CONFIG_FILE_NAMES[0])
        self.has_config_file = False

        self.config_dir = self.get_config_dir()
        self.config_file = self.get_config_file()
        self._config_content = None

    @property
    def config_content(self):
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

    def get_config_dir(self) -> str:
        """

        Args:

        Returns:

        Raises:

        """
        env_config_dir = os.environ.get("GRAI_CLI_CONFIG_DIR", None)

        if env_config_dir is not None and os.path.exists(env_config_dir):
            return env_config_dir

        for path in self.config_paths:
            if os.path.exists(path):
                return path

        os.mkdir(self.default_config_path)
        return self.default_config_path

    def get_config_file(self) -> Optional[str]:
        """

        Args:

        Returns:

        Raises:

        """
        for file_name in self.DEFAULT_CONFIG_FILE_NAMES:
            file = os.path.join(self.config_dir, file_name)
            if os.path.exists(file):
                self.has_config_file = True
                return file

        return self.default_config_file


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
        settings (BaseSettings):

    Returns:

    Raises:

    """
    if not config_handler.has_config_file:
        return {}
    file = config_handler.config_file
    with open(file, "r") as file:
        result = yaml.safe_load(file)
    return result if result is not None else {}


class ServerSettingsV1(BaseModel):
    """ """

    api_version: Literal["v1"] = "v1"
    host: str = "localhost"
    port: str = "8000"
    workspace: str
    insecure: bool = False

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


class GraiConfig(YamlModelMixin, BaseSettings):
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
            """

            Args:
                init_settings:
                env_settings:
                file_secret_settings:

            Returns:

            Raises:

            """
            return (
                init_settings,
                env_settings,
                yaml_config_settings_source,
            )


if config_handler.has_config_file:
    try:
        config = GraiConfig()
    except Exception as e:
        message = f"Unable to construct a complete config file from provided environment variables and/or the config file located at {config_handler.config_file}"
        raise Exception(message) from e
else:
    _default_config = {
        "auth": {
            "username": "null@grai.io",
            "password": "super_secret",
        },
        "server": {
            "host": "localhost",
            "port": "8000",
            "insecure": True,
            "workspace": "default",
        },
    }
    config = GraiConfig(**_default_config)
