import os
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def process_video(video_path, background_path, output_dir, segment_length=61):
    video = VideoFileClip(video_path)
    background_video = VideoFileClip(background_path)

    duration = int(video.duration)
    num_segments = duration // segment_length
    extra_seconds = duration % segment_length

    segments = []
    start = 0

    for i in range(num_segments):
        end = start + segment_length
        if i == num_segments - 1:  # Add the extra seconds to the last segment
            end += extra_seconds
        
        segment = video.subclip(start, end)

        # Resize segment to fit top half with a slight shrink
        segment = segment.resize(height=background_video.size[1] // 2 * 0.9)
        
        # Choose a random start point for the background segment
        max_background_start = background_video.duration - segment.duration
        background_start = random.uniform(0, max_background_start)
        background_segment = background_video.subclip(background_start, background_start + segment.duration)
        
        # Composite the segment onto the background
        composite_segment = CompositeVideoClip([background_segment, segment.set_position(('center', 'top'))])

        # Calculate crop dimensions for 9:16 aspect ratio
        video_width, video_height = composite_segment.size
        target_width = video_height * 9 / 16
        crop_x1 = (video_width - target_width) / 2
        crop_x2 = crop_x1 + target_width

        # Ensure target width is a multiple of 2 for the codec
        if target_width % 2 != 0:
            target_width += 1
            crop_x2 = crop_x1 + target_width

        composite_segment = composite_segment.crop(x1=crop_x1, x2=crop_x2)

        # Calculate text size and position
        fontsize = int(composite_segment.size[1] / 8)  # Approximately 1/8th of the video height
        txt_clip = TextClip(f"Part {i + 1}", fontsize=fontsize, color='white', stroke_color='black', stroke_width=2)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(segment.duration)

        # Create the composite video with the text overlay
        final_segment = CompositeVideoClip([composite_segment, txt_clip])

        segment_filename = os.path.join(output_dir, f"segment_{i + 1}.mp4")
        final_segment.write_videofile(segment_filename, codec='libx264', preset='fast')
        print(f"Saved: {segment_filename}")

        segments.append(segment_filename)
        start = end

    # Remove the original video after processing
    os.remove(video_path)

    # Remove any leftover .mp3 files in the directory
    for file in os.listdir(output_dir):
        if file.endswith('.mp3'):
            os.remove(os.path.join(output_dir, file))

    return segments
