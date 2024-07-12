import os
import subprocess

def convert_segments_to_mov(folder_path, text):
    output_folder = os.path.join(folder_path, "./../aivoiceovers")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    mp4_file_path = os.path.join(folder_path, 'final_video.mp4')
    mp3_file_path = os.path.join(folder_path, 'output.mp3')
    first_five_words = '_'.join(text.split()[:5])
    mov_file_name = f"{first_five_words}.mov"
    mov_file_path = os.path.join(output_folder, mov_file_name)
    
    p = subprocess.run(
        [
            "ffmpeg",
            "-i", mp4_file_path,
            "-n",
            "-acodec", "copy",
            "-vcodec", "copy",
            "-f", "mov", mov_file_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=False
    )
    
    if p.returncode == 0:
        os.remove(mp4_file_path)
        os.remove(mp3_file_path)
        print(f"Converted {mp4_file_path} to {mov_file_path}")
    else:
        print(f"Failed to convert {mp4_file_path}")
