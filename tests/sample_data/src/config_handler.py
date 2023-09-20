import configparser
import logging
from typing import Union
import os


class ConfigHandler:
    def __init__(self, config_file: Union[str, None] = None):
        self.config = configparser.ConfigParser()
        if config_file:
            self.config.read(config_file)
        elif "FOLDERINFO_CONFIG" in os.environ:
            self.config.read(os.environ["FOLDERINFO_CONFIG"])
        else:
            self.config.read("default_config.ini")
            logging.info("Using default configuration.")

    def get(self, section: str, option: str) -> str:
        try:
            return self.config.get(section, option)
        except configparser.NoSectionError as e:
            logging.error(f"Section not found in configuration: {e}")
        except configparser.NoOptionError as e:
            logging.error(f"Option not found in configuration: {e}")
