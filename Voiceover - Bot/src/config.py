import os
import toml

CONFIG_FILE = 'config.toml'

def read_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found. Please run setup.py first.")
    
    with open(CONFIG_FILE, 'r') as file:
        config = toml.load(file)
    
    return config

def write_config(config):
    with open(CONFIG_FILE, 'w') as file:
        toml.dump(config, file)
