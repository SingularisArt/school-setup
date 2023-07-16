import json
from pathlib import Path

import yaml


def load_data(data_file, type):
    config_file = Path(data_file).expanduser()
    if not config_file.exists():
        return False

    config_file_open = open(config_file, "r").read()

    if type == "yaml":
        try:
            return yaml.safe_load(config_file_open)
        except yaml.YAMLError:
            return False
    elif type == "json":
        try:
            return json.load(config_file_open)
        except json.decoder.JSONDecodeError:
            return False
    else:
        raise
