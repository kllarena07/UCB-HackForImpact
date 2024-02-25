import os
import requests
from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import assemblyai as aai
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("TWELVELABS_API_URL")
TASKS_URL = f"{API_URL}/tasks"

app = Flask(__name__)

def prunes_files():
    if os.path.exists("./imported_video.mp4"):
        os.remove("./imported_video.mp4")
        
    if os.path.exists("./extracted_audio.mp3"):
        os.remove("./extracted_audio.mp3")

def transcribe():
    aai.settings.api_key = os.getenv("AAI_API_KEY")

    FILE_URL = "./extracted_audio.mp3"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        print(transcript.text)

def extract_audio():
    video_clip = VideoFileClip("./imported_video.mp4")
    audio_clip = video_clip.audio

    audio_output_path = "./extracted_audio.mp3"
    audio_clip.write_audiofile(audio_output_path)

    video_clip.close()
    transcribe()
    
    prunes_files()

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file.save("imported_video.mp4")
    extract_audio()
    
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
