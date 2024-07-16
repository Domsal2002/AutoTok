from openai import OpenAI
import requests
import json
import os
import random
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to read keywords from a file
def read_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file.readlines()]
    return keywords

# Function to sanitize text by removing escape characters and unnecessary formatting
def sanitize_text(text):
    # Remove escape characters
    text = text.encode('latin1').decode('unicode_escape')
    # Remove any extra spaces or new lines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to generate a story using OpenAI GPT
def generate_story(keyword, category, language):
    if language == "Spanish":
        category_translation = {
            "AITA": "¿Soy el malo?",
            "TIFU": "Hoy metí la pata"
        }
        prompt = (
            f"Please keep the story engaging and intriguing but under one minute of talking time"
            f"¿Puedes escribir una publicación intrigante de Reddit '{category_translation[category]}' que incluya la palabra clave '{keyword}'? "
            f"La publicación debe tener un título llamativo, seguido por el contenido principal de la historia, separado por '...'. "
            f"Debe ser apta para el trabajo (SFW) pero interesante de una manera adulta. "
            f"No incluyas la palabra 'título'. Formatea el resultado como {{título}} ... {{historia}}. "
            f"Por favor, haz esto en español. Mantén el mismo formato y usa la intuición para traducir palabras y frases que no tienen traducciones directas. "
            f"Puedes traducir la palabra clave '{keyword}' si es necesario para que tenga sentido en la historia. "
            f"Asegúrate de que el resultado no contenga caracteres adicionales o secuencias de escape."
        )
    else:
        prompt = (
            f"Can you write an intriguing Reddit {category} post that includes the keyword '{keyword}'? "
            f"The post should have a compelling title, followed by the main content of the story, separated by '...'. "
            f"It should be safe for work (SFW) but interesting in an adult manner. "
            f"Do not include the word 'title'. Format the output as {{title}} ... {{story}}. Ensure the output contains no additional characters or escape sequences."
        )

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7)
        story_content = response.choices[0].message.content.strip()
        print("Raw response content:", story_content)  # Debugging line

        # Split the story content into title and body
        if '...' in story_content:
            title, body = story_content.split('...', 1)
            title = sanitize_text(title.strip().strip('"').strip('{}'))
            body = sanitize_text(body.strip().strip('"').strip('{}'))
        else:
            title = "No Title"
            body = sanitize_text(story_content.strip())

        return {"title": title, "body": body}

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return {"title": "Error", "body": "OpenAI API error occurred"}

# Function to post the story to the database
def post_story_to_db(story, language):
    if language == "Spanish":
        url = "http://127.0.0.1:5000/data/spanish"
    else:
        url = "http://127.0.0.1:5000/data/english"

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(story))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return {"status": "error", "message": str(e)}

def main():
    language = input("Would you like to generate prompts in English or Spanish? ").strip().capitalize()
    if language not in ["English", "Spanish"]:
        print("Invalid choice. Please choose either 'English' or 'Spanish'.")
        return

    keywords = read_keywords('keywords.txt')
    num_prompts = int(input("How many prompts would you like to create? "))

    for _ in range(num_prompts):
        category = random.choice(["AITA", "TIFU"])
        keyword = random.choice(keywords)
        story = generate_story(keyword, category, language)
        result = post_story_to_db(story, language)
        print(result)

if __name__ == "__main__":
    main()
