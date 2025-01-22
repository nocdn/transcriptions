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
from dotenv import load_dotenv

load_dotenv()

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS', '{m4a, mp3, wav}')
DEFAULT_GEMINI_PROMPT = os.environ.get('DEFAULT_GEMINI_PROMPT', '')
DEFAULT_GEMINI_MODEL = os.environ.get('DEFAULT_GEMINI_MODEL', 'gemini-2.0-flash-exp')

# API Keys
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
FIREWORKS_API_KEY = os.environ.get('FIREWORKS_API_KEY')


if load_dotenv():
    print("Loaded .env file")
else:
    print("Failed to load .env file.")

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
    logging.info(f'Processing with Gemini:')
    logging.info(f'Model: {gemini_model}')
    logging.info(f'Prompt: {gemini_prompt}')
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

def process_with_fireworks(filepath, model="fireworks/whisper-v3-turbo", language="en"):
    logging.info(f'Processing with Fireworks:')
    logging.info(f'Model: {model}')
    logging.info(f'Language: {language}')
    correct_model = model.replace("fireworks/", "")
    logging.info(f'Using correct model name: {correct_model}')
    try:
        with open(filepath, "rb") as f:
            response = requests.post(
                "https://audio-turbo.us-virginia-1.direct.fireworks.ai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {FIREWORKS_API_KEY}"},
                files={"file": f},
                data={
                    "model": correct_model,
                    "temperature": "0",
                    "vad_model": "silero",
                    "language": language
                }
            )
            
        if response.status_code == 200:
            return response.json().get('text', '')
        else:
            raise Exception(f"Fireworks API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        logging.error(f'Error processing with Fireworks: {str(e)}')
        raise

def process_with_groq(filepath, model, language="en", prompt=""):
    logging.info(f'Processing with Groq:')
    logging.info(f'Model: {model}')
    logging.info(f'Language: {language}')
    logging.info(f'Prompt: {prompt}')
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
            provider = request.form.get('currentModelProvider')
            if provider == 'groq':
                model = request.form.get('groqModelValue')
                prompt = request.form.get('groqPromptValue')
                language = request.form.get('groqLanguageValue')
                result = process_with_groq(filepath, model, language, prompt)
            elif provider == 'gemini':
                model = request.form.get('geminiModelValue')
                prompt = request.form.get('geminiPromptValue')
                if prompt == '':
                    prompt = DEFAULT_GEMINI_PROMPT
                result = process_with_gemini(filepath, model, prompt)
            elif provider == 'fireworks':
                model = request.form.get('fireworksModelValue')
                language = request.form.get('fireworksLanguageValue')
                result = process_with_fireworks(filepath, model, language)


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