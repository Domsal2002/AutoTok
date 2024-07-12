import os
import json
import random

# Load backgrounds
with open('backgrounds.json') as f:
    backgrounds = json.load(f)

def ensure_background_video_exists(background_info):
    background_path = os.path.join('backgrounds', background_info[1])
    if not os.path.exists(background_path):
        raise FileNotFoundError(f"Background video {background_path} not found. Please ensure all backgrounds are downloaded.")
    return background_path

def choose_random_background():
    background_key = random.choice(list(backgrounds.keys()))
    background_info = backgrounds[background_key]
    background_path = ensure_background_video_exists(background_info)
    return background_path
