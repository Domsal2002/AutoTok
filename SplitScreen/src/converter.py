import os
import subprocess

def convert_segments_to_mov(folder_path):
    for fn in os.listdir(folder_path):
        if fn.endswith(".mp4"):
            file_path = os.path.join(folder_path, fn)
            print("mp4 file found: " + file_path)
            mov_file_path = os.path.join(folder_path, fn[:-4] + ".mov")
            
            p = subprocess.run(
                [
                    "ffmpeg",
                    "-i", file_path,
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
                os.remove(file_path)
                print("Converted " + file_path)
            else:
                print("Skipped " + file_path)
