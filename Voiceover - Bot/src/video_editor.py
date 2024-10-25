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
    char_index = 0

    for word in words:
        word_start_time = None
        word_end_time = None
        for char in word:
            while (char_index < len(characters) and characters[char_index] in [' ', '\n']):
                char_index += 1
            if char_index < len(characters) and characters[char_index] == char:
                if word_start_time is None:
                    word_start_time = start_times[char_index]
                word_end_time = end_times[char_index]
                char_index += 1
            else:
                logging.error(f"Character '{char}' not found in alignment at index {char_index}.")
                raise Exception(f"Could not find timing information for character: {char}")
        if word_start_time is not None and word_end_time is not None:
            word_duration = word_end_time - word_start_time
            timing_info.append((word, word_start_time, word_duration))
        else:
            logging.error(f"Timing information missing for word '{word}'.")
            raise Exception(f"Could not find timing information for word: {word}")

    logging.debug(f"Timing info: {timing_info}")
    return timing_info

def generate_subtitle_clips(timing_info, video_width, video_height):
    clips = []
    for word, start_time, duration in timing_info:
        txt_clip = TextClip(word, fontsize=70, color='white', size=(video_width, None), method='caption',
                            stroke_color='black', stroke_width=2)
        txt_clip = txt_clip.set_duration(duration).set_pos('center').set_start(start_time)
        clips.append(txt_clip)
    return clips

def adjust_timing_for_body_subtitles(timing_info, title_duration):
    adjusted_timing_info = []
    for word, start_time, duration in timing_info:
        adjusted_start_time = start_time + title_duration
        adjusted_timing_info.append((word, adjusted_start_time, duration))
    return adjusted_timing_info

def get_audio_duration(audio_file_path):
    audio = AudioFileClip(audio_file_path)
    return audio.duration

def edit_video(background_path, title, body, config):
    video = VideoFileClip(background_path)
    
    # Generate voiceover for title and body separately
    title_audio_file_path, _ = generate_voiceover_with_timestamps(title, config, is_title=True)
    body_audio_file_path, body_alignment = generate_voiceover_with_timestamps(body, config)
    
    # Combine audio files
    combined_audio_path = 'combined_output.mp3'
    concat_command = f"ffmpeg -i \"concat:{title_audio_file_path}|{body_audio_file_path}\" -acodec copy {combined_audio_path}"
    os.system(concat_command)
    
    audio = AudioFileClip(combined_audio_path)
    
    video_duration = video.duration
    audio_duration = audio.duration

    max_start_time = video_duration - audio_duration
    start_time = random.uniform(0, max_start_time)

    video = video.subclip(start_time, start_time + audio_duration)

    target_aspect_ratio = 9/16
    video = video.resize(height=1080)
    video = video.crop(x_center=video.w / 2, width=video.h * target_aspect_ratio, height=video.h)

    title_duration = get_audio_duration(title_audio_file_path)
    body_timing_info = analyze_audio_timing_with_alignment(body_alignment, body)
    adjusted_body_timing_info = adjust_timing_for_body_subtitles(body_timing_info, title_duration)
    subtitle_clips = generate_subtitle_clips(adjusted_body_timing_info, video.w, video.h)
    
    final_video = CompositeVideoClip([video] + subtitle_clips).set_audio(audio)
    final_video_path = 'final_video.mp4'
    final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac')
    
    return final_video_path, combined_audio_path
