import os
import random
import logging
import requests
from src.config import read_config
from src.video_editor import edit_video
from src.converter import convert_segments_to_mov

def choose_random_background():
    """Choose a random background video from the backgrounds folder."""
    backgrounds_folder = './utils/backgrounds'
    background_files = [f for f in os.listdir(backgrounds_folder) if f.endswith('.mp4')]
    if not background_files:
        raise FileNotFoundError("No background files found in the backgrounds folder.")
    return os.path.join(backgrounds_folder, random.choice(background_files))

def fetch_data(language):
    """Fetch data from the local API based on the selected language."""
    url = f'http://127.0.0.1:5000/data/{language}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def delete_entry(entry_id, language):
    """Delete an entry from the local API based on the selected language."""
    url = f'http://127.0.0.1:5000/data/{language}?id={entry_id}'
    response = requests.delete(url)
    response.raise_for_status()

def process_video(entry, language, config):
    """Process a single video entry."""
    title = entry["title"]
    body = entry["body"]
    logging.debug(f"Selected entry ID: {entry['id']} - Text for voiceover: {body}")

    if not body:
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
        final_video, audio_file = edit_video(background_path, title, body, config)
        logging.debug(f"Edited video: {final_video}")
    except Exception as e:
        logging.error(f"Error editing video: {e}")
        return

    # Convert to MOV format
    try:
        folder_path = os.path.dirname(final_video)
        convert_segments_to_mov(folder_path, body, language)
        logging.info("Converted all segments to MOV format and cleaned up temporary files")
    except Exception as e:
        logging.error(f"Error converting video to MOV: {e}")

    # Delete the entry after processing
    try:
        delete_entry(entry["id"], language)
        logging.info(f"Deleted entry ID: {entry['id']}")
    except Exception as e:
        logging.error(f"Error deleting entry: {e}")

def main():
    logging.basicConfig(level=logging.DEBUG)
    config = read_config()

    language = input("Choose language (english/spanish): ").strip().lower()
    if language not in ["english", "spanish"]:
        logging.error("Invalid language choice. Please choose 'english' or 'spanish'.")
        return

    try:
        video_count = int(input("How many videos do you want to create? ").strip())
        created_videos = 0

        while created_videos < video_count:
            try:
                data = fetch_data(language)
                if not data:
                    logging.info("No more data available from the API.")
                    break

                entry = random.choice(data)
                process_video(entry, language, config)
                created_videos += 1
                logging.info(f"Successfully created video {created_videos} of {video_count}")

            except Exception as e:
                logging.error(f"Error during video processing: {e}")
                break

    except Exception as e:
        logging.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
