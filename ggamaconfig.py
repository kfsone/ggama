from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import toml

@dataclass
class Config:
    """ Container for runtime configuration values loaded from args/env/file in that order. """
    vector_file: Path

    openai_api_key: str

    github_token: str
    github_user: str
    github_repos: str
    github_branch: str

    github_dirs: Optional[dict[str]]
    github_extensions: Optional[dict[str]]

    _config_dict: dict
    _config_file: Path = Path("ggama.user.toml")
    _fields = (
        ("general", ("vector_file",)),
        ("openai",  ("api_key",)),
        ("github",  ("token", "user", "repos", "branch", "dirs", "extensions")),
    )

    @classmethod
    def _get_fields(cls):
        """ Internal helper that yields the list of key names """
        for section, keys in cls._fields:
            for key in keys:
                kwarg_name = f"{section}_{key}" if section != 'general' else key
                env_name   = f"{section if section != 'general' else 'ggama'}_{key}".upper()
                yield (section, key), kwarg_name, env_name

    def _get_values(self, **kwargs):
        """ Internal helper that determines the current preferred configuration properties """
        for (section, key), kwarg_name, env_name in self._get_fields():
            if kwarg_name in kwargs:
                yield kwarg_name, kwargs[kwarg_name]
            elif env_name in os.environ:
                yield kwarg_name, os.getenv(env_name)
            else:
                try:
                    yield kwarg_name, self._config_dict[section][key]
                except KeyError:
                    raise KeyError(f"No {kwarg_name} argument, ${env_name}, and no {section}.{key} in {self._config_file}")

    def __init__(self, **kwargs) -> None:
        self._config_dict = {} if not self._config_file.exists() else toml.load(self._config_file.open("r"))
        for name, value in self._get_values(**kwargs):
            if name == "vector_file":
                setattr(self, name, Path(value))
            else:
                setattr(self, name, value)

        os.putenv("OPENAI_API_KEY", self.openai_api_key)
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
