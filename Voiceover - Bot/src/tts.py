import requests
import json
import base64
import logging

def generate_voiceover_with_timestamps(text, config):
    voice_id = config['ELEVEN_LABS_VOICE']
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    
    headers = {
        "xi-api-key": config['ELEVEN_LABS_API_KEY'],
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    logging.debug(f"Sending request to Eleven Labs API with data: {json.dumps(data)}")
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    response_dict = response.json()
    logging.debug(f"Response from Eleven Labs API: {response_dict}")
    
    # Decode the audio file
    audio_bytes = base64.b64decode(response_dict["audio_base64"])
    audio_file_path = 'output.mp3'
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio_bytes)
    
    # Extract alignment information
    alignment = response_dict['alignment']
    
    return audio_file_path, alignment