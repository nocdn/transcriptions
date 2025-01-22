# Transcriptions

This is a full stack web app built with Svelte, Tailwind, Flask that can be self hosted, and offers a simple way to transcribe audio files.

## Features

- Supports 3 model providers: Groq (Whisper models), Google (Gemini multimodal) and FireworksAI (Whisper model)
- BYOK - Bring your own keys
- Provides a transcription history
- Saves settings between wesite visits
- Supports multiple audio file formats
- Supports multiple languages
- Supports multiple speaker diarization

## Setup

#### Prerequisites

You must have the following installed on your machine:

- [npm](https://www.npmjs.com/)
- [Python](https://www.python.org/)

Clone the repository

```bash
git clone https://github.com/nocdn/transcription-svelte.git
```

Install the dependencies

```bash
cd transcription-svelte
npm install
```

Configure your API keys and settings by copying the `.env.example` file to `.env` and filling it in with your own values.

```bash
cp .env.example .env
```

Start the front-end development server

```bash
npm run dev
```

In a new terminal, start the back-end development server

```bash
cd transcription-svelte/src/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
