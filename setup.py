import toml
from pathlib import Path

TEMPLATE_FILE = Path('./Utils/.config.template.toml')
CONFIG_FILE = Path('config.toml')

def load_template(file_path):
    """Load the TOML template file."""
    try:
        with open(file_path, 'r') as file:
            return toml.load(file)
    except FileNotFoundError:
        print(f"Template file {file_path} not found.")
        return None

def write_config(config, file_path):
    """Write the configuration to a TOML file."""
    with open(file_path, 'w') as file:
        toml.dump(config, file)

def ask_for_value(key, details):
    """Ask the user for a value, displaying relevant details."""
    default = details.get('default', None)
    example = details.get('example', None)
    explanation = details.get('explanation', "")
    required = details.get('optional', False) is False
    prompt = f"{explanation} (Default: {default}, Example: {example})\nEnter {key}: "

    value = input(prompt).strip()

    if not value and required:
        print(f"{key} is required. Please provide a value.")
        return ask_for_value(key, details)
    return value or default

def populate_config(config):
    """Recursively populate the config dictionary by asking the user for inputs."""
    for section, items in config.items():
        if isinstance(items, dict):
            for key, details in items.items():
                if isinstance(details, dict) and 'explanation' in details:
                    config[section][key] = ask_for_value(f"{section}.{key}", details)
                elif isinstance(details, dict):
                    # Recurse into nested sections
                    populate_config({key: details})
        else:
            print(f"Skipping unknown format for section: {section}")

def setup_config():
    """Setup the configuration by referencing a template and asking the user for input."""
    config = load_template(TEMPLATE_FILE)
    if config is None:
        return
    
    print("Please fill in the configuration details:")
    populate_config(config)
    
    # Write the updated configuration to the output file
    write_config(config, CONFIG_FILE)
    print(f"Configuration written to {CONFIG_FILE}")

if __name__ == "__main__":
    setup_config()
