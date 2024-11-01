import openai
from openai import OpenAI
import json
import re
import toml  # Assuming your config file is in TOML format
from data_handler import sanitize_input

# Load configuration from a .toml file
config = toml.load('./../config.toml')

# Access the settings from the config file
client = OpenAI(api_key=config['settings']['chatgpt']['OPENAI_API_KEY'])

CATEGORY_TRANSLATIONS = {
    'spanish': {
        "AITA": "¿Soy el malo?",
        "TIFU": "Hoy metí la pata"
    },
    'english': {
        "AITA": "Am I the Asshole",
        "TIFU": "Today I Fucked Up"
    }
}

def generate_story(language, category):
    if language not in CATEGORY_TRANSLATIONS or category not in CATEGORY_TRANSLATIONS[language]:
        raise ValueError("Invalid language or category")

    category_prompt = CATEGORY_TRANSLATIONS[language][category]

    if language == 'spanish':
        prompt = (
            f"Por favor, escribe un post breve e intrigante de Reddit '{category_prompt}'. "
            f"El post debe tener un título llamativo y un contenido principal de la historia. "
            f"Formatea el resultado como un objeto JSON con dos campos: 'title' y 'story'. "
            f"Asegúrate de que la historia esté en español, sea adecuada para todos los públicos pero interesante para adultos, y esté orientada a una audiencia latinoamericana. "
            f"Usa la letra 'Ñ' cuando sea necesario. "
            f"Asegúrate de que el resultado sea un JSON válido y no contenga caracteres adicionales o secuencias de escape."
        )
    else:
        prompt = (
            f"Can you write a brief and captivating Reddit '{category_prompt}' post? "
            f"The post should have a compelling title and the main content of the story. "
            f"Format the output as a JSON object with two fields: 'title' and 'story'. "
            f"Ensure the story is SFW but interesting in an adult manner and suitable for an American audience. "
            f"Make sure the output is valid JSON and contains no additional characters or escape sequences."
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a storyteller."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        story_content = response.choices[0].message.content.strip()
        print("Raw response content:", story_content)
        return story_content  # Return raw content for processing

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None  # Return None to indicate failure
