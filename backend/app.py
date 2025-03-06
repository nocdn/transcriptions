import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from flask_cors import CORS
from groq import Groq
import google.generativeai as genai
from pathlib import Path
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import requests
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS', '{m4a, mp3, wav}')
DEFAULT_GEMINI_PROMPT = os.environ.get('DEFAULT_GEMINI_PROMPT', '')
DEFAULT_GEMINI_MODEL = os.environ.get('DEFAULT_GEMINI_MODEL', 'gemini-2.0-flash')

# API Keys
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
FIREWORKS_API_KEY = os.environ.get('FIREWORKS_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

# Rate limits
TRANSCRIPTION_RATE_LIMIT = os.environ.get('TRANSCRIPTION_RATE_LIMIT', '10 per day')
HISTORY_RATE_LIMIT = os.environ.get('HISTORY_RATE_LIMIT', '1000 per day')
DELETE_RATE_LIMIT = os.environ.get('DELETE_RATE_LIMIT', '1000 per day')

if load_dotenv():
    print("Loaded .env file")
else:
    print("Failed to load .env file.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per day"],
    storage_uri="memory://",
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)

elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

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

def process_with_elevenlabs(filepath, model="scribe_v1"):
    logging.info(f'Processing with Groq:')
    logging.info(f'Model: {model}')
    try:
        elevenlabs_transcription = elevenlabs_client.speech_to_text.convert(file=filepath, model=model, language_code="eng")
        return elevenlabs_transcription.text
    except Exception as e:
        logging.error(f'Error processing with ElevenLabs: {str(e)}')
        raise


@app.route('/api/upload', methods=['POST'])
@limiter.limit(TRANSCRIPTION_RATE_LIMIT)
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
@limiter.limit(HISTORY_RATE_LIMIT)
def get_history():
    try:
        history = []
        history_path = Path('history')
        if history_path.exists():
            for file in history_path.glob('*.txt'):
                creation_time = file.stat().st_ctime
                from datetime import datetime
                formatted_date = datetime.fromtimestamp(creation_time).strftime('%d-%m-%Y')
                # extract the file extension from the stem (which might contain original file extension)
                filename_parts = file.stem.split('.')
                file_extension = filename_parts[-1] if len(filename_parts) > 1 else ""
                # get filename without extension for the new key
                filename_no_ext = '.'.join(filename_parts[:-1]) if len(filename_parts) > 1 else file.stem

                history.append({
                    'filename': file.stem,
                    'transcription': file.read_text(),
                    'date': formatted_date,
                    'fileExtension': file_extension,
                    'fileNameNoExt': filename_no_ext
                })
        return jsonify(history)
    except Exception as e:
        logging.error(f'Error getting history: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete', methods=['POST'])
@limiter.limit(DELETE_RATE_LIMIT)
def delete_history_item():
    try:
        data = request.json
        if not data or 'filename' not in data:
            return jsonify({'error': 'Filename is required'}), 400

        filename = data['filename']
        # Sanitize the filename to prevent directory traversal attacks
        safe_filename = secure_filename(filename)
        file_path = Path(f'history/{safe_filename}.txt')

        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        # Delete the file
        file_path.unlink()

        return jsonify({'success': True, 'message': f'Deleted {filename}'})

    except Exception as e:
        logging.error(f'Error deleting history item: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # create required directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('history', exist_ok=True)

    app.run(host='0.0.0.0', port=6005)
