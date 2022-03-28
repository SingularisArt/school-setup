import yaml
from pathlib import Path


def load_data():
    """
    Loads the data from a config.yaml file. It first checks if there
    exists a config.yaml file in ~/.config/lesson-manager/ and if not,
    it just loads the default config.yaml file.

    Returns:
        data (dict): The data from the config.yaml file.
    """

    # Check if there exists a ~/.config/lesson-manager/config.yaml file
    # If not, use the default config.yaml file which is located
    # ./config.yaml
    config_file = Path('~/.config/lesson-manager/config.yaml').expanduser()
    if not config_file.exists():
        config_file = Path('./config.yaml')

    # Load all of the data from the config file
    with open(config_file, 'r') as config_file_open:
        try:
            data = yaml.safe_load(config_file_open)
        except yaml.YAMLError as exc:
            raise exc

    # Return the data from the config file
    return data
