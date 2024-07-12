import os
import random
import logging
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from src.tts import generate_voiceover_with_timestamps

def analyze_audio_timing_with_alignment(alignment, text):
    characters = alignment['characters']
    start_times = alignment['character_start_times_seconds']
    end_times = alignment['character_end_times_seconds']
    
    words = text.split()
    timing_info = []
    current_time = 0
    char_index = 0
    
    for word in words:
        word_start_time = None
        word_end_time = None
        for char in word:
            while char_index < len(characters) and characters[char_index] == ' ':
                char_index += 1
            if char_index < len(characters) and characters[char_index] == char:
                if word_start_time is None:
                    word_start_time = start_times[char_index]
                word_end_time = end_times[char_index]
                char_index += 1
        if word_start_time is not None and word_end_time is not None:
            word_duration = word_end_time - word_start_time
            timing_info.append((word, word_start_time, word_duration))
        else:
            raise Exception(f"Could not find timing information for word: {word}")

    logging.debug(f"Timing info: {timing_info}")
    return timing_info

def generate_subtitle_clips(timing_info, video_width, video_height):
    clips = []
    for word, start_time, duration in timing_info:
        txt_clip = TextClip(word, fontsize=70, color='white', size=(video_width, None), method='caption')
        txt_clip = txt_clip.set_duration(duration).set_pos('center').set_start(start_time)
        clips.append(txt_clip)
    logging.debug(f"Generated subtitle clips: {clips}")
    return clips

def edit_video(background_path, text, config):
    logging.debug(f"Editing video with background {background_path}")
    video = VideoFileClip(background_path)
    
    audio_file_path, alignment = generate_voiceover_with_timestamps(text, config)
    logging.debug(f"Generated audio file: {audio_file_path}")
    
    audio = AudioFileClip(audio_file_path)
    
    video_duration = video.duration
    audio_duration = audio.duration

    max_start_time = video_duration - audio_duration
    start_time = random.uniform(0, max_start_time)

    logging.debug(f"Video duration: {video_duration}, Audio duration: {audio_duration}, Start time: {start_time}")

    # Trim video to the length of the audio file
    video = video.subclip(start_time, start_time + audio_duration)

    # Convert to 9:16 aspect ratio
    target_aspect_ratio = 9/16
    video = video.resize(height=1080)
    video = video.crop(x_center=video.w / 2, width=video.h * target_aspect_ratio, height=video.h)

    timing_info = analyze_audio_timing_with_alignment(alignment, text)
    subtitle_clips = generate_subtitle_clips(timing_info, video.w, video.h)
    
    final_video = CompositeVideoClip([video] + subtitle_clips).set_audio(audio)
    final_video_path = 'final_video.mp4'
    final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac')
    
    logging.debug(f"Final video path: {final_video_path}")
    return final_video_path, audio_file_path
