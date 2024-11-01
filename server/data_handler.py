import json
import os
import logging
import unicodedata
import string
import re

json_files = {
    'english': os.getenv('ENGLISH_JSON_PATH', 'English.json'),
    'spanish': os.getenv('SPANISH_JSON_PATH', 'Spanish.json'),
}

def read_json_file(language):
    try:
        with open(json_files[language], 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading {language} JSON file: {e}")
        return []

def write_json_file(language, data):
    try:
        with open(json_files[language], 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        logging.error(f"Error writing to {language} JSON file: {e}")

def sanitize_input(data):
    sanitized_data = {}
    allowed_punctuation = '.?!¿¡'
    allowed_letters = 'ÑñáéíóúüÁÉÍÓÚÜ'

    for key, value in data.items():
        if isinstance(value, str):
            normalized_value = ''.join(
                char if char in allowed_letters else unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('ascii')
                for char in value
            )
            sanitized_value = ''.join(
                char for char in normalized_value
                if char in string.ascii_letters + string.digits + string.whitespace + allowed_punctuation + allowed_letters
            )
            sanitized_value = re.sub(r'\s+([{}])'.format(re.escape(allowed_punctuation)), r'\1', sanitized_value)
            sanitized_data[key] = sanitized_value
        else:
            sanitized_data[key] = value
    return sanitized_data

