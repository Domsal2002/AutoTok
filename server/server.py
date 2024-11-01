from flask import Flask, request, jsonify, send_from_directory
import uuid
import logging
from data_handler import read_json_file, write_json_file, sanitize_input
from gptPrompter import generate_story
import json

app = Flask(__name__, static_folder='static')

# Set up logging
logging.basicConfig(level=logging.INFO)

VALID_LANGUAGES = ['english', 'spanish']
VALID_CATEGORIES = ['AITA', 'TIFU']

@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():
    # Accept input data as JSON
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    language = data.get('language', 'english').lower()
    category = data.get('category', 'AITA').upper()

    if language not in VALID_LANGUAGES or category not in VALID_CATEGORIES:
        return jsonify({"error": "Invalid language or category"}), 400

    # Generate the story
    story_content = generate_story(language, category)

    if story_content is None:
        return jsonify({"error": "OpenAI API error occurred"}), 500

    # Parse the JSON output
    try:
        story_json = json.loads(story_content)
        title = story_json.get('title', 'No Title')
        body = story_json.get('story', '')
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        title = "No Title"
        body = story_content  # Use the entire content as the body

    # Create the story dictionary
    story = {"title": title, "body": body}

    # Assign a unique ID
    story['id'] = str(uuid.uuid4())

    # Sanitize the story
    sanitized_story = sanitize_input(story)

    # Read current data, append new story, and write back
    current_data = read_json_file(language)
    current_data.append(sanitized_story)
    write_json_file(language, current_data)

    # Return the sanitized story
    return jsonify(sanitized_story)

@app.route('/')
def index():
    logging.debug("Attempting to serve index.html")
    return send_from_directory('static', 'index.html')

@app.route('/data/<language>', methods=['GET'])
def get_stories(language):
    language = language.lower()
    if language not in VALID_LANGUAGES:
        return jsonify({"error": "Invalid language"}), 400

    stories = read_json_file(language)
    return jsonify(stories)

@app.route('/delete_story', methods=['DELETE'])
def delete_story():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    language = data.get('language', '').lower()
    story_id = data.get('id', '')

    if language not in VALID_LANGUAGES or not story_id:
        return jsonify({"error": "Invalid language or story ID"}), 400

    stories = read_json_file(language)
    updated_stories = [story for story in stories if story.get('id') != story_id]

    if len(stories) == len(updated_stories):
        return jsonify({"error": "Story not found"}), 404

    write_json_file(language, updated_stories)

    return jsonify({"message": "Story deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
