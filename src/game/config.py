from dynaconf import Dynaconf
from dynaconf import loaders
from dynaconf.utils.boxing import DynaBox


import os

configFilePath = os.path.join("config", "config_new.toml")

config = Dynaconf(
    settings_files = [configFilePath]
)

def set_config(category, setting, value):
    config[category][setting] = value

def save_config(filepath = configFilePath):
    config_dict = config.as_dict()
    loaders.write(filepath, DynaBox(config_dict).to_dict())

if __name__ == "__main__":
    print(config.as_dict())
    
