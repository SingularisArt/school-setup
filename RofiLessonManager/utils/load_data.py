#!/usr/bin/env python3

import json
from pathlib import Path
import yaml


def load_data(data_file: str, type: str) -> dict:
    """
    Load the data from given file.

    Args:
        data_file (str): The location to the yaml file you wish to load.
        type (str): Type of data file: yaml, json

    Returns:
        data (dict): The data from the yaml data file file.

    Raises:
        FileNotFoundError: If the given file doesn't exist.
        YAMLError: If there's an error loading the actual data from the given
            yaml data file.
        JSONDecodeError: If there's an error loading the actual data from the
            given json data file.
    """

    # Check if the data file exists.
    config_file = Path(data_file).expanduser()
    # If not, raise an error.
    if not config_file.exists():
        raise FileNotFoundError(f"File {data_file} couldn't be loaded.")

    # Load all of the data from the config file.
    config_file_open = open(config_file, "r").read()

    if type == "yaml":
        try:
            # Return the data from the config file.
            return yaml.safe_load(config_file_open)
        except yaml.YAMLError as exc:
            raise exc
    elif type == "json":
        try:
            # Return the data from the config file.
            return json.load(config_file_open)
        except json.decoder.JSONDecodeError as exc:
            raise exc
    else:
        raise
