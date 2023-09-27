import importlib.resources as pkg_resources
import os
import platform
import warnings
from itertools import product
from pprint import pprint
from typing import Any, Dict, Literal, Optional, Protocol, Union

import typer
import yaml
from goodconf import Field, GoodConf
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    BaseSettings,
    EmailStr,
    PrivateAttr,
    SecretStr,
)


class EnvironmentVariables:
    config_file = "GRAI_CLI_CONFIG"


def default_config_paths():
    operating_system = platform.system()
    if operating_system == "Darwin":
        home_path = os.path.expanduser("~")
        config_path = [f"{home_path}/.config/grai"]
    elif operating_system == "Linux":
        home_path = os.path.expanduser("~")
        config_path = [f"{home_path}/.config/grai"]
    elif operating_system == "Windows":
        home_path = os.getenv("APPDATA")
        config_path = [f"{home_path}/grai"]
    elif operating_system == "":
        raise Exception("Python could not detect the type of your operating system. ")
    else:
        warnings.warn(
            f"Operating system {operating_system} not recognized. Expected either 'Darwin', 'Windows', or 'Linux'"
        )
        home_path = os.path.expanduser("~")
        config_path = [f"{home_path}/.config/grai"]
    return config_path


def get_config_file_from_environment(search_paths) -> str:
    default_names = ["config.yaml", "config.yml"]
    config_file = os.environ.get(EnvironmentVariables.config_file, None)
    if config_file is None:
        found_file = False
        for path, filename in product(search_paths, default_names):
            config_file = os.path.join(path, filename)
            if found_file := os.path.exists(config_file):
                break
        if not found_file:
            config_file = os.path.join(search_paths[0], default_names[0])
    return config_file


class ConfigDirHandler:
    def __init__(self, config_file: Optional[str] = None):
        self.search_paths = default_config_paths()
        if config_file is None:
            config_file = get_config_file_from_environment(self.search_paths)

        self.config_file = config_file
        self.config_dir = os.path.dirname(self.config_file)
        os.makedirs(self.config_dir, exist_ok=True)

    @property
    def has_config_file(self):
        return os.path.exists(self.config_file)


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


class ServerSettingsV1(BaseModel):
    """ """

    api_version: Literal["v1"] = "v1"
    url: AnyHttpUrl
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
    username: EmailStr
    password: SecretStr


class ApiKeySettings(AuthModeSettings):
    """ """

    authentication_mode: Literal["api_key"] = "api_key"
    api_key: SecretStr


class ContextSettings(BaseModel):
    """ """

    namespace: str = "default"


class LazyConfig(GoodConf):
    _loaded = PrivateAttr(False)
    _emit_warning = PrivateAttr(True)

    def __init__(self, load=False, **kwargs):
        self._loaded = load
        kwargs.setdefault("load", load)
        super().__init__(**kwargs)

    def __getattr__(self, name):
        if not self._loaded:
            self.load()
            self._loaded = True
            return getattr(self, name)

        raise ValueError(f"{self} does not have attribute `{name}`")


def load_warning():
    message = (
        f"\nWe were unable to construct a complete config file from provided environment variables and/or the config file "
        f"located at {config_handler.config_file}. This most likely means either \n"
        f"1) The config file is malformed, in which case you can edit it or execute `grai config init` to recreate it.\n"
        f"2) The config directory is incorrect. We've attempted looking in the following directories: "
        f"{config_handler.search_paths} based on your operating system and the `{EnvironmentVariables.config_file}` env "
        f"var. \n"
        f"3) You may have made a mistake configuring your environment based purely on environment variables: \n"
    )
    warnings.warn(message)


class BaseGraiConfig(LazyConfig):
    class Config:
        default_files = [config_handler.config_file]
        file_env_var = EnvironmentVariables.config_file
        validate_assignment = True

    def load(self, filename: Optional[str] = None, with_warning=True) -> None:
        try:
            super().load(filename)
        except Exception as e:
            load_warning()
            default_config = str(pkg_resources.files("grai_cli") / "config_default.yaml")
            super().load(filename=default_config)

        self._config_file = self.__config__._config_file

    @property
    def config_location(self):
        if not self._loaded:
            self.load()
        return self._config_file

    @classmethod
    def from_file(cls, file):
        with open(file, "r") as file:
            content = yaml.safe_load(file)
        return cls(**content)

    def save(self, save_path: Optional[str] = None):
        """ """
        values = unredact(self.dict())
        save_path = save_path if save_path is not None else config_handler.config_file

        with open(save_path, "w") as f:
            yaml.dump(values, f)

    def view(self):
        """ """

        def redact(obj: dict) -> dict:
            """ """
            if isinstance(obj, dict):
                return {k: redact(v) for k, v in obj.items()}
            elif isinstance(obj, SecretStr):
                return str(obj)
            else:
                return obj

        if not self._loaded:
            self.load()
        data = redact(self.dict())
        data_representation = yaml.dump(data, default_flow_style=False)
        return data_representation


class GraiConfig(BaseGraiConfig):
    server: Union[ServerSettingsV1]
    auth: Union[BasicAuthSettings, ApiKeySettings]


config = GraiConfig()
