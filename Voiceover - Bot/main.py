import os
import random
import logging
from src.config import read_config
from src.video_editor import edit_video
from src.converter import convert_segments_to_mov

def choose_random_background():
    backgrounds_folder = './../backgrounds'
    background_files = [f for f in os.listdir(backgrounds_folder) if f.endswith('.mp4')]
    return os.path.join(backgrounds_folder, random.choice(background_files))

def main():
    logging.basicConfig(level=logging.DEBUG)
    config = read_config()
    
    text = input("Enter the text for the voiceover: ")
    logging.debug(f"Text for voiceover: {text}")
    
    if not text:
        logging.error("No text provided for the voiceover.")
        return
    
    # Select a random background
    try:
        background_path = choose_random_background()
        logging.debug(f"Selected background: {background_path}")
    except Exception as e:
        logging.error(f"Error selecting background: {e}")
        return
    
    # Edit video
    try:
        final_video, audio_file = edit_video(background_path, text, config)
        logging.debug(f"Edited video: {final_video}")
    except Exception as e:
        logging.error(f"Error editing video: {e}")
        return
    
    # Convert to MOV format
    try:
        folder_path = os.path.dirname(final_video)
        convert_segments_to_mov(folder_path, text)
        logging.info("Converted all segments to MOV format and cleaned up temporary files")
    except Exception as e:
        logging.error(f"Error converting video to MOV: {e}")

if __name__ == "__main__":
    main()
