"""Load the configuration."""

import dataclasses
import os
import tomllib


class ConfigLoadError(Exception):
    """Raised when an error ocurrs while reading/loading the configuration."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConfDef:
    """The Python definition of a default configuration."""

    host: str
    port: str
    clsc_ids_json: str = "~/.clscidapi/clsc_ids.json"
    ssl_certfile: str | None = None
    ssl_keyfile: str | None = None
    log_config: str | None = None
    log_level: dict | None = None
    api_debug: bool = False
    max_classic_ids: int = 56400


class Config(ConfDef):
    """The loaded application config.

    Once loaded, object is read-only.

    Handles defaults by passing all items in the loaded
    config file to ``ConfDef`` as keyword args.

    Parameters
    ----------
    path : str, optional
        The path to the config file, by default "config.toml"

    Raises
    ------
    ConfigLoadError
        If ``Config`` cannot find the file or, the config
        caused an error when loaded by ``ConfDef``.
    """

    def __init__(self, path="~/.clscidapi/config.toml") -> None:
        path = os.path.expandvars(os.path.expanduser(path))
        try:
            with open(path, "rb") as conf_file:
                loaded_toml = tomllib.load(conf_file)
            super().__init__(**loaded_toml)
        except (OSError, TypeError) as err:
            raise ConfigLoadError(
                f"Unable to load config from ({path}): {err}"
            ) from err
