from openai import OpenAI
import requests
import json
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to sanitize text by removing escape characters and unnecessary formatting
def sanitize_text(text):
    # Remove escape characters
    text = text.encode('latin1').decode('unicode_escape')
    # Remove any extra spaces or new lines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to translate and adjust the title for Spanish
def translate_title(title):
    prompt = f"Translate and adjust the following title to make sense in Spanish for a Reddit post: '{title}'. Ensure it is compelling and fits the context of a Reddit story."
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.7
        )
        translated_title = response.choices[0].message.content.strip()
        return sanitize_text(translated_title)
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return title

# Function to generate a story using OpenAI GPT
def generate_story_body(custom_title, language, story_length):
    if language == "Spanish":
        if story_length == "long":
            prompt = (
                f"Escribe una historia de Reddit con el título '{custom_title}'. "
                f"La historia debe durar entre 2 y 5 minutos al ser leída en voz alta, "
                f"y debe ser como un episodio de un programa de telerrealidad, llena de drama y giros inesperados, pero lo suficientemente realista para ser creíble. "
                f"Asegúrate de que la historia esté en español, sea adecuada para todos los públicos pero interesante para adultos, y esté orientada a una audiencia latinoamericana. "
                f"Usa la letra 'Ñ' cuando sea necesario. "
                f"Asegúrate de que el resultado no contenga caracteres adicionales o secuencias de escape."
            )
            max_tokens = 4096
        else:
            prompt = (
                f"Escribe una historia de Reddit con el título '{custom_title}'. "
                f"La historia debe durar como máximo 1 minuto al ser leída en voz alta, "
                f"y debe ser como un episodio de un programa de telerrealidad, llena de drama y giros inesperados, pero lo suficientemente realista para ser creíble. "
                f"Asegúrate de que la historia esté en español, sea adecuada para todos los públicos pero interesante para adultos, y esté orientada a una audiencia latinoamericana. "
                f"Usa la letra 'Ñ' cuando sea necesario. "
                f"Asegúrate de que el resultado no contenga caracteres adicionales o secuencias de escape."
            )
            max_tokens = 300
    else:
        if story_length == "long":
            prompt = (
                f"Can you write a Reddit story with the title '{custom_title}'? "
                f"The story should take between 2 and 5 minutes to read aloud, "
                f"and should feel like an episode of a reality TV show, full of drama and unexpected twists, but realistic enough to be believable. "
                f"Ensure the story is SFW but interesting in an adult manner. "
                f"Ensure the output contains no additional characters or escape sequences."
            )
            max_tokens = 4096
        else:
            prompt = (
                f"Can you write a Reddit story with the title '{custom_title}'? "
                f"The story should take a maximum of 1 minute to read aloud. Ensure this by making the story around 120 words long. "
                f"The story should feel like an episode of a reality TV show, full of drama and unexpected twists, but realistic enough to be believable. "
                f"Ensure the story is SFW but interesting in an adult manner and suitable for an American audience. "
                f"Ensure the output contains no additional characters or escape sequences."
            )
            max_tokens = 500

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7
        )
        story_content = response.choices[0].message.content.strip()
        print("Raw response content:", story_content)  # Debugging line

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return {"title": "Error", "body": "OpenAI API error occurred"}

    body = sanitize_text(story_content.strip())

    return {"title": custom_title, "body": body}

# Function to post the story to the database
def post_story_to_db(story, language, story_length):
    if language == "Spanish":
        if story_length == "long":
            url = "http://127.0.0.1:5000/data/spanish_long"
        else:
            url = "http://127.0.0.1:5000/data/spanish"
    else:
        if story_length == "long":
            url = "http://127.0.0.1:5000/data/english_long"
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

    story_length = input("Do you want the story to be long? (yes/no) ").strip().lower()
    if story_length not in ["yes", "no"]:
        print("Invalid choice. Please choose either 'yes' or 'no'.")
        return
    story_length = "long" if story_length == "yes" else "short"

    custom_title = input("What do you want the title of the story to be? ").strip()
    if language == "Spanish":
        custom_title = translate_title(custom_title)

    num_prompts = int(input("How many prompts would you like to create? "))

    for _ in range(num_prompts):
        story = generate_story_body(custom_title, language, story_length)
        result = post_story_to_db(story, language, story_length)
        print(result)

if __name__ == "__main__":
    main()
