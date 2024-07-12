import os
import json
import yt_dlp

def download_youtube_video(url, output_path, output_name):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_path, output_name),
        'cookiefile': 'cookies.txt',
        'geo_bypass': True,
        'age_verify': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return os.path.join(output_path, output_name)

def main():
    json_file_path = 'backgrounds.json'
    
    if not os.path.exists(json_file_path):
        print(f"JSON file {json_file_path} does not exist.")
        return
    
    with open(json_file_path, 'r') as file:
        video_data = json.load(file)

    output_path = 'backgrounds'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for key, value in video_data.items():
        url = value[0]
        output_name = value[1]
        output_file_path = os.path.join(output_path, output_name)

        if not os.path.exists(output_file_path):
            print(f"Downloading {output_name} from {url}")
            download_youtube_video(url, output_path, output_name)
        else:
            print(f"{output_name} already exists, skipping download.")

if __name__ == "__main__":
    main()
