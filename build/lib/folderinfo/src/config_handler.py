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

    def _read_config_from_path(self, path: str):
        try:
            self.config.read(path)
        except Exception as e:
            logging.error(f"Error reading configuration from {path}: {e}")

    def _read_config_from_content(self, content: Union[list, dict]):
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

    def get(self, section: str, option: str) -> Optional[str]:
        """Get a specific option from a section.

        Args:
        - section (str): The section in the configuration.
        - option (str): The option within the section.

        Returns:
        - str or None: The value of the option if it exists.
        """
        try:
            return self.config.get(section, option)
        except configparser.NoSectionError as e:
            logging.error(f"Section not found in configuration: {e}")
            return None
        except configparser.NoOptionError as e:
            logging.error(f"Option not found in configuration: {e}")
            return None

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
