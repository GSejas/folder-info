import configparser
import logging
from typing import Union, Optional
import os
from io import StringIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "default_config.ini")

logging.basicConfig(level=logging.INFO)


class ConfigHandler:
    """Handles reading configurations from files and environment variables."""

    def __init__(
        self,
        config_input: Optional[Union[str, list, dict]] = None,
        use_env_var: bool = True,
    ):
        self.config = configparser.ConfigParser()

        if isinstance(config_input, str) and os.path.exists(config_input):
            self._read_config_from_path(config_input)
        elif isinstance(config_input, (list, dict)):
            self._read_config_from_content(config_input)
        elif use_env_var and "FOLDERINFO_CONFIG" in os.environ:
            env_path = os.environ["FOLDERINFO_CONFIG"]
            if os.path.exists(env_path):
                self._read_config_from_path(env_path)
            else:
                logging.warning(
                    f"Environment variable 'FOLDERINFO_CONFIG' points to a non-existent path: {env_path}. Falling back to default configuration."
                )
                self._read_config_from_path(DEFAULT_CONFIG_PATH)
        else:
            self._read_config_from_path(DEFAULT_CONFIG_PATH)
            logging.info("Using default configuration.")

    def get(self, section, key, fallback=None):
        """
        The `get` function retrieves a value from a configuration file, handling errors if the section or
        option is not found.

        :param section: The `section` parameter is a string that represents the section name in the
        configuration file. Sections are used to group related configuration options together
        :param key: The `key` parameter is a string that represents the option key within a section of the
        configuration file. It is used to retrieve the value associated with that key
        :param fallback: The `fallback` parameter is an optional argument that specifies the value to return
        if the specified `section` or `key` is not found in the configuration. If no `fallback` value is
        provided, `None` will be returned by default
        :return: The `get` method returns the value of the specified `key` in the specified `section` of the
        configuration. If the `section` or `key` is not found, it logs an error message and returns `None`.
        """
        try:
            return self.config.get(section, key, fallback=fallback)
        except configparser.NoSectionError as e:
            logging.error(f"Section not found in configuration: {e}")
            return None
        except configparser.NoOptionError as e:
            logging.error(f"Option not found in configuration: {e}")
            return None

    def _read_config_from_path(self, path: str):
        try:
            self.config.read(path)
        except Exception as e:
            logging.error(f"Error reading configuration from {path}: {e}")

    def _read_config_from_content(self, content: Union[list, dict]):
        """
        The `_read_config_from_content` function reads configuration data from a content object (either a
        dictionary or a list) and converts it into a format that can be read by the `config` object.

        :param content: The `content` parameter can be either a list or a dictionary
        :type content: Union[list, dict]
        """
        try:
            # Si es un diccionario, convierte a formato .ini

            if isinstance(content, dict):
                content_str = self._dict_to_ini_format(content)
            elif isinstance(content, list):
                content_str = "\n".join(content)
            else:
                raise ValueError("Invalid content type for configuration.")

            # Convertir content_str en un objeto similar a un archivo para leer
            file_like_content = StringIO(content_str)
            self.config.read_file(file_like_content)
        except Exception as e:
            logging.error(f"Error reading configuration from content: {e}")

    def get_sections(self) -> list:
        """Retrieve a list of sections in the configuration."""
        return self.config.sections()

    def has_option(self, section: str, option: str) -> bool:
        """Check if an option exists within a section."""
        return self.config.has_option(section, option)

    def has_section(self, section: str) -> bool:
        """Check if a section exists."""
        return self.config.has_section(section)

    def _dict_to_ini_format(self, content: dict) -> str:
        output = []
        for section, entries in content.items():
            output.append(f"[{section}]")
            for key, value in entries.items():
                output.append(f"{key} = {value}")
        return "\n".join(output)
