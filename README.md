# ** I am currently working on making this repository more readable and useable as its current state does not make it extremely friendly to someone who is not familiar with its core functionality and workflow. ** 

# AI-Generated Reddit Story Video Creator

This project leverages OpenAI's GPT-4 to generate AI-driven Reddit-style stories and automatically edits them into videos formatted for YouTube Shorts. The project is designed to create engaging and captivating content by combining AI-generated narratives with video editing techniques.

## Core Functionality

1. **Story Generation**: Utilizes OpenAI's GPT-4 to generate Reddit-style stories based on user input or random selection. The stories can be in English or Spanish and vary in length.

2. **Video Editing**: Automatically edits the generated stories into video format using MoviePy, adding subtitles and voiceovers to create a complete video ready for upload.

3. **Voiceover Generation**: Uses Eleven Labs API to generate voiceovers for the story titles and bodies, ensuring a professional audio experience.

4. **Video Conversion**: Converts the final video into MOV format, suitable for various platforms.

5. **Data Management**: Manages story data using a local Flask server, storing and retrieving stories in JSON format.

## Technologies Used

- **Python**: The primary programming language used for scripting and automation.
- **OpenAI GPT-4**: For generating AI-driven stories.
- **Flask**: A lightweight web framework used to create a local server for data management.
- **MoviePy**: A Python library for video editing.
- **Eleven Labs API**: For generating voiceovers with timestamps.
- **FFmpeg**: A multimedia framework used for video conversion.
- **PIL (Pillow)**: For image processing and text overlay on thumbnails.

## APIs Used

- **OpenAI API**: To interact with GPT-4 for story generation.
- **Eleven Labs API**: For text-to-speech conversion to create voiceovers.

## How It Works

1. **Story Creation**: The user inputs a keyword or selects a category, and the system generates a story using GPT-4.
2. **Voiceover and Subtitles**: The story is converted into a voiceover, and subtitles are generated based on the text.
3. **Video Editing**: A random background video is selected, and the story is overlaid with subtitles and voiceover.
4. **Video Conversion**: The final video is converted to MOV format and saved.
5. **Data Management**: The story data is stored and managed using a local Flask server.

## Sample Video

Check out a sample video created by this project on YouTube: [Watch Here](https://www.youtube.com/shorts/SRaHOkfT_NE)

## Code Structure

- **Gpt-Query**: Contains scripts for generating stories using GPT-4.
- **Voiceover - Bot**: Handles video editing, voiceover generation, and video conversion.
- **server**: Manages story data using a Flask server.
- **Thumbnail Generator Imager**: Generates thumbnails with text overlay.

## License

This project is licensed under the MIT License.
