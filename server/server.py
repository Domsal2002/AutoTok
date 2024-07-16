from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os
import uuid
import logging
import unicodedata
import string
import re

app = Flask(__name__)
api = Api(app)

# Paths to your local JSON files
json_files = {
    'english': os.getenv('ENGLISH_JSON_PATH', 'English.json'),
    'spanish': os.getenv('SPANISH_JSON_PATH', 'Spanish.json'),
    'english_long': os.getenv('ENGLISH_LONG_JSON_PATH', 'English_long.json'),
    'spanish_long': os.getenv('SPANISH_LONG_JSON_PATH', 'Spanish_long.json')
}

# Function to read JSON file
def read_json_file(language):
    try:
        with open(json_files[language], 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading {language} JSON file: {e}")
        return []

# Function to write to JSON file
def write_json_file(language, data):
    try:
        with open(json_files[language], 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        logging.error(f"Error writing to {language} JSON file: {e}")

# Function to sanitize input data
def sanitize_input(data):
    sanitized_data = {}
    allowed_punctuation = '.?!¿'
    allowed_letters = 'Ñ'
    
    for key, value in data.items():
        if isinstance(value, str):
            # Normalize and remove non-ASCII characters
            normalized_value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
            # Keep only ASCII letters, digits, whitespace, and allowed punctuation
            sanitized_value = ''.join(
                char for char in normalized_value 
                if char in string.ascii_letters + string.digits + string.whitespace + allowed_punctuation + allowed_letters
            )
            # Ensure punctuation is directly attached to the preceding word
            sanitized_value = re.sub(r'\s+([{}])'.format(re.escape(allowed_punctuation)), r'\1', sanitized_value)
            sanitized_data[key] = sanitized_value
        else:
            sanitized_data[key] = value
    return sanitized_data

class DataResource(Resource):
    def get(self, language):
        if language in json_files:
            data = read_json_file(language)
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({"error": "Invalid language"}), 400)

    def post(self, language):
        if language in json_files:
            new_data = request.json
            if isinstance(new_data, dict) and 'title' in new_data and 'body' in new_data and len(new_data) == 2:
                new_data = sanitize_input(new_data)
                new_data['id'] = str(uuid.uuid4())
                current_data = read_json_file(language)
                if not isinstance(current_data, list):
                    current_data = []
                current_data.append(new_data)
                write_json_file(language, current_data)
                return make_response(jsonify({"message": "Data added successfully", "id": new_data['id']}), 200)
            else:
                return make_response(jsonify({"error": "Invalid data format. Only 'title' and 'body' fields are allowed"}), 400)
        else:
            return make_response(jsonify({"error": "Invalid language"}), 400)

    def delete(self, language):
        if language in json_files:
            data_id = request.args.get('id')
            if data_id:
                current_data = read_json_file(language)
                updated_data = [item for item in current_data if item.get('id') != data_id]
                if len(current_data) == len(updated_data):
                    return make_response(jsonify({"error": "ID not found"}), 404)
                write_json_file(language, updated_data)
                return make_response(jsonify({"message": "Data deleted successfully"}), 200)
            else:
                return make_response(jsonify({"error": "ID not provided"}), 400)
        else:
            return make_response(jsonify({"error": "Invalid language"}), 400)

class DeleteAllResource(Resource):
    def delete(self, language):
        if language in json_files:
            write_json_file(language, [])
            return make_response(jsonify({"message": "All data deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Invalid language"}), 400)

api.add_resource(DataResource, '/data/<string:language>')
api.add_resource(DeleteAllResource, '/data/<string:language>/delete_all')

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Local JSON Server"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    # Initialize JSON files with an empty list if they don't exist
    for lang, path in json_files.items():
        if not os.path.exists(path):
            with open(path, 'w') as file:
                json.dump([], file)
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    app.run(debug=True)
