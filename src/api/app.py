import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from groq import Groq
import google.generativeai as genai
from pathlib import Path
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import requests

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'m4a', 'mp3', 'wav'}
DEFAULT_GEMINI_PROMPT = "Transcribe this exactly, DO NOT add timestamps, diarize the speakers, call the Interviewer just 'Interviewer' and the other person 'Candidate'"
DEFAULT_GEMINI_MODEL = 'models/gemini-1.5-flash'

# API Keys
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyAnuQo93v9AIkxoD3tOYPuT9uEOiaMqmNQ"
FIREWORKS_API_KEY = "cQlEpRGJbif9YQMGwGH8HWmUG1kkbBalQAumk6KMjLm9tFTF"

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_history_file(filename, content):
    history_file = Path(f'history/{filename}')
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with open(history_file, 'w') as f:
        f.write(content)

def process_with_gemini(filepath, gemini_model, gemini_prompt):
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(gemini_model)
        
        audio_file = genai.upload_file(filepath)
        result = model.generate_content([audio_file, gemini_prompt],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            })
        
        audio_file.delete()
        return result.text
    except Exception as e:
        logging.error(f'Error processing with Gemini: {str(e)}')
        raise

def process_with_fireworks(filepath, model="accounts/fireworks/models/whisper-v3-turbo"):
    try:
        with open(filepath, "rb") as f:
            response = requests.post(
                "https://audio-turbo.us-virginia-1.direct.fireworks.ai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {FIREWORKS_API_KEY}"},
                files={"file": f},
                data={
                    "model": model,
                    "temperature": "0",
                    "vad_model": "silero"
                }
            )
            
        if response.status_code == 200:
            return response.json().get('text', '')
        else:
            raise Exception(f"Fireworks API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        logging.error(f'Error processing with Fireworks: {str(e)}')
        raise

def process_with_groq(filepath, model, language=None, prompt=None):
    try:
        transcription_params = {
            'file': (os.path.basename(filepath), open(filepath, 'rb')),
            'response_format': 'json',
            'temperature': 0.0
        }

        if model:
            transcription_params['model'] = model
        if language:
            transcription_params['language'] = language
        if prompt:
            transcription_params['prompt'] = prompt

        transcription = groq_client.audio.transcriptions.create(**transcription_params)
        transcription_params['file'][1].close()
        
        return transcription.text.lstrip()
    except Exception as e:
        logging.error(f'Error processing with Groq: {str(e)}')
        raise

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Unsupported file type'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            provider = request.form.get('model_provider', 'groq')
            model = request.form.get('model')
            language = request.form.get('language')
            prompt = request.form.get('prompt')

            if provider == 'gemini':
                result = process_with_gemini(filepath, model or DEFAULT_GEMINI_MODEL, 
                                          prompt or DEFAULT_GEMINI_PROMPT)
            elif provider == 'fireworks':
                result = process_with_fireworks(filepath, model)
            else:  # default to groq
                result = process_with_groq(filepath, model, language, prompt)

            save_history_file(f"{filename}.txt", result)
            return jsonify({'transcription': result})

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = {}
        history_path = Path('history')
        if history_path.exists():
            for file in history_path.glob('*.txt'):
                history[file.stem] = file.read_text()
        return jsonify(history)
    except Exception as e:
        logging.error(f'Error getting history: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create required directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('history', exist_ok=True)
    
    app.run(host='0.0.0.0', port=6005)