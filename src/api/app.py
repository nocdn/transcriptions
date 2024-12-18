import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from groq import Groq
import google.generativeai as genai
from pathlib import Path
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)
groq_client = Groq(api_key="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")

# Configure file upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'m4a', 'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DEFAULT_GEMINI_PROMPT = "Transcribe this exactly, DO NOT add timestamps, diarize the speakers, call the Interviewer just 'Interviewer' and the other person 'Candidate'"
DEFAULT_GEMINI_MODEL = 'models/gemini-1.5-flash'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Enhanced logging setup with formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_with_gemini(filepath, gemini_model, gemini_prompt):
    try:
        # Configure Gemini API

        genai.configure(api_key="AIzaSyAnuQo93v9AIkxoD3tOYPuT9uEOiaMqmNQ")
        model = genai.GenerativeModel(gemini_model)

        # Upload and process the audio file
        audio_file = genai.upload_file(filepath)
        result = model.generate_content([audio_file, gemini_prompt],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            })

        # Clean up
        audio_file.delete()

        return result.text
    except Exception as e:
        logging.error(f'Error processing with Gemini: {str(e)}')
        raise

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Log all form data at the start
    logging.info("Received request with the following parameters:")
    for key in request.form:
        logging.info(f"  {key}: {request.form[key]}")

    if 'file' not in request.files:
        logging.error('No file part in the request')
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error('No file selected')
        return jsonify({'error': 'No file selected'}), 400

    # Get parameters from request
    process_gemini = request.form.get('process_gemini', 'false').lower() == 'true'
    gemini_model = request.form.get('gemini_model', DEFAULT_GEMINI_MODEL)
    gemini_prompt = request.form.get('gemini_prompt', DEFAULT_GEMINI_PROMPT)

    # Groq parameters
    model = request.form.get('model')
    language = request.form.get('language')
    prompt = request.form.get('prompt')

    # Log the processed parameters
    logging.info("Processing with parameters:")
    logging.info(f"  Process with Gemini: {process_gemini}")
    if process_gemini:
        logging.info(f"  Gemini Model: {gemini_model}")
        logging.info(f"  Gemini Prompt: {gemini_prompt}")
    else:
        logging.info(f"  Groq Model: {model}")
        logging.info(f"  Language: {language}")
        logging.info(f"  Prompt: {prompt}")
    logging.info(f"  File: {file.filename}")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logging.info(f'Saving file to {filepath}')
        file.save(filepath)

        try:
            if process_gemini:
                # Process with Gemini
                logging.info(f'Starting Gemini processing for {filename}')
                result = process_with_gemini(filepath, gemini_model, gemini_prompt)
                response_data = {'transcription': result}
            else:
                # Process with Groq
                logging.info(f'Starting Groq transcription for {filename}')
                transcription_params = {
                    'file': (filename, open(filepath, 'rb')),
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
                response_data = {'transcription': transcription.text}

            # Clean up
            logging.info(f'Deleting file {filepath}')
            os.remove(filepath)

            if not os.path.exists(filepath):
                logging.info(f'File {filename} successfully deleted')
            else:
                logging.error(f'Failed to delete file {filename}')

            return jsonify(response_data)

        except Exception as e:
            logging.error(f'Error processing file {filename}: {str(e)}')
            # Ensure file is deleted in case of error
            if os.path.exists(filepath):
                logging.info(f'Deleting file {filepath} after error')
                try:
                    os.remove(filepath)
                    logging.info(f'File {filename} successfully deleted after error')
                except Exception as delete_error:
                    logging.error(f'Failed to delete file {filename} after error: {str(delete_error)}')
            return jsonify({'error': str(e)}), 500
    else:
        logging.error(f'Unsupported file type: {file.filename}')
        return jsonify({'error': 'Unsupported file type'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6005)