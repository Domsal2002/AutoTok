from openai import OpenAI
import requests
import json
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to generate a story using OpenAI GPT
def generate_story(keyword):
    prompt = (
        f"Can you please produce an alluring Reddit story that replicates Reddit AITA? "
        f"It should be SFW but also intriguing and interesting in an adult manner. "
        f"Please output it in a valid JSON format with the tags 'title' and 'body'. "
        f"Ensure the output is a well-formed JSON string with double quotes around keys and values. "
        f"Include the keyword '{keyword}' in the story."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    story_content = response.choices[0].message.content.strip()
    print("Raw response content:", story_content)  # Debugging line

    # Attempt to clean and parse the JSON response
    try:
        # Ensure it starts and ends with curly braces
        if not story_content.startswith("{"):
            story_content = "{" + story_content.split("{", 1)[1]
        if not story_content.endswith("}"):
            story_content = story_content.rsplit("}", 1)[0] + "}"

        story_json = json.loads(story_content)
    except json.JSONDecodeError as e:
        print("Error decoding JSON from OpenAI response:", e)
        story_json = {"title": "Error", "body": "Could not decode the response from OpenAI"}

    # Add a unique ID to the story
    story_json['id'] = str(uuid.uuid4())
    return story_json

# Function to post the story to the database
def post_story_to_db(story):
    url = "http://127.0.0.1:5000/data/english"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(story))
    return response.json()

def main():
    keyword = input("Please enter a keyword for the story: ")
    story = generate_story(keyword)
    result = post_story_to_db(story)
    print(result)

if __name__ == "__main__":
    main()
