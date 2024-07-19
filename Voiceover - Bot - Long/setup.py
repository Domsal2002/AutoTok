import toml

CONFIG_FILE = 'config.toml'

def write_config(config):
    with open(CONFIG_FILE, 'w') as file:
        toml.dump(config, file)

if __name__ == "__main__":
    config = {
        'ELEVEN_LABS_API_KEY': "YOUR_API_KEY_HERE",
        'ELEVEN_LABS_VOICE': "YOUR_VOICE_ID_HERE"
    }
    write_config(config)
    print(f"Configuration written to {CONFIG_FILE}")
