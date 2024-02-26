import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import assemblyai as aai
from dotenv import load_dotenv
load_dotenv()

def prune_audio_file():    
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

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    prune_audio_file()
    try:
        audio_file = request.files['audio']
        
        # Save the audio file
        audio_file.save("extracted_audio.mp3")
        print("Audio file saved as: extracted_audio.mp3")
        
        transcribe()
        
        return jsonify({'message': 'Audio file received and saved successfully'})
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
