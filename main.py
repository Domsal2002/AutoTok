import os
from src.downloader import download_youtube_video
from src.backgrounds import choose_random_background
from src.video_processor import process_video
from src.converter import convert_segments_to_mov

def main():
    youtube_url = input("Enter the YouTube video URL: ")
    output_path = 'videos'
    
    video_path = download_youtube_video(youtube_url, output_path)
    
    # Get the video's title from the downloaded path
    video_folder_name = os.path.basename(video_path).rsplit('.', 1)[0]
    video_folder_path = os.path.join(output_path, video_folder_name)
    
    # Create a folder for the video
    if not os.path.exists(video_folder_path):
        os.makedirs(video_folder_path)
    
    # Move the downloaded video to its folder
    new_video_path = os.path.join(video_folder_path, os.path.basename(video_path))
    os.rename(video_path, new_video_path)
    
    background_path = choose_random_background()
    
    process_video(new_video_path, background_path, video_folder_path)
    
    # Convert the processed segments to .mov format
    convert_segments_to_mov(video_folder_path)

if __name__ == "__main__":
    main()
