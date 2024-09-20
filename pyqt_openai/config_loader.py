import configparser
import os
import shutil

import yaml

from pyqt_openai import CONFIG_DATA, INI_FILE_NAME, get_config_directory, ROOT_DIR, SRC_DIR

_config_cache = None


def parse_value(value):
    # Boolean conversion
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    # Numeric conversion
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            pass
    # Default: return the value as is (string)
    return value

def convert_list(value):
    # Convert comma-separated string to list
    return [item.strip() for item in value.split(',')]

def init_yaml():
    yaml_data = CONFIG_DATA

    config_dir = get_config_directory()
    config_path = os.path.join(config_dir, INI_FILE_NAME)

    if not os.path.exists(config_path):
        # Save as YAML file
        with open(config_path, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False)
    else:
        with open(config_path, 'r') as yaml_file:
            prev_yaml_data = yaml.safe_load(yaml_file)
        # Add new keys
        for section, values in yaml_data.items():
            if section not in prev_yaml_data:
                prev_yaml_data[section] = values
            else:
                for key, value in values.items():
                    if key not in prev_yaml_data[section]:
                        prev_yaml_data[section][key] = value
        # Save as YAML file
        with open(config_path, 'w') as yaml_file:
            yaml.dump(prev_yaml_data, yaml_file, default_flow_style=False)


class ConfigManager:
    def __init__(self, yaml_file=INI_FILE_NAME):
        self.yaml_file = yaml_file
        self.config = self._load_yaml()

    def _load_yaml(self):
        with open(self.yaml_file, 'r') as file:
            return yaml.safe_load(file)

    def _save_yaml(self):
        with open(self.yaml_file, 'w') as file:
            yaml.safe_dump(self.config, file)

    # Getter methods
    def get_general(self):
        return self.config.get('General', {})

    def get_general_property(self, key):
        return self.config.get('General', {}).get(key)

    def set_general_property(self, key, value):
        if 'General' not in self.config:
            self.config['General'] = {}
        self.config['General'][key] = value
        self._save_yaml()

# TODO WILL_REMOVE_AFTER v1.2.0
prev_config_path = os.path.join(ROOT_DIR, 'config.yaml') if os.path.exists(os.path.join(ROOT_DIR, 'config.yaml')) else (os.path.join(SRC_DIR, 'config.yaml') if os.path.exists(os.path.join(SRC_DIR, 'config.yaml')) else None)
if prev_config_path:
    new_config_path = os.path.join(get_config_directory(), INI_FILE_NAME)
    if not os.path.exists(new_config_path):
        shutil.move(prev_config_path, new_config_path)
else:
    pass

init_yaml()
CONFIG_MANAGER = ConfigManager()
# print(CONFIG_MANAGER.get_general_property('API_KEY'))