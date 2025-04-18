# Transcriptions

> a full stack web app built with Svelte, Tailwind, Flask that can be self hosted with docker compose, and offers a simple way to transcribe audio files

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Features

- Supports 4 model providers:
  - `Groq` (inferencing OpenAI Whisper) - cheapest, medium speed, medium accuracy
  - `Google` (through gemini audio multimodality) - cheapest/medium price, slower speed, high accuracy
  - `FireworksAI` (inferencing OpenAI Whisper) - medium price, fastest speed, semi-high accuracy
  - `ElevenLabs` (in-house Scribe model) - most expensive, slowest speed, highest accuracy
- Saves a transcription history
- Saves settings between frontend visits
- Supports multiple audio file formats
- Supports multiple languages
- Supports multiple speaker diarization
- Can return word level or segment level timestamps
- BYOK - Bring your own keys

### Preview

![Main](main.png)
![Settings](settings.png)

### Setup

#### Option 1: Docker Setup (Recommended)

##### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

Clone the repository

```bash
git clone https://github.com/nocdn/transcriptions.git
cd transcriptions
```

Configure your API keys and settings by copying the `.env.example` file to `.env` and filling it in with your own values.

```bash
cp .env.example .env
```

Build and start the Docker containers.

```bash
docker compose up -d --build
```

Depending on where you host it, the application will be available at `http://localhost:4090` or `http://[your-machine-ip]:4090`

##### Updating (if using Docker)

Stop the containers:

```bash
docker compose down
```

Pull the latest changes:

```bash
git pull
```

Build and start the Docker containers again:

```bash
docker compose up -d --build
```

#### Option 2: Local Development

##### Prerequisites

You must have the following installed on your machine:

- [npm](https://www.npmjs.com/)
- [Python](https://www.python.org/)

Clone the repository:

```bash
git clone https://github.com/nocdn/transcriptions.git
```

Install the frontend dependencies:

```bash
cd transcriptions/frontend
npm install
```

From the same directory, start the front-end development server:

```bash
npm run dev
```

For the backend:

Configure your API keys and settings by copying the `.env.example` file to `.env` and filling it in with your own values.

```bash
cd transcriptions/backend
cp .env.example .env
```

In a new terminal, start the back-end development server:

```bash
cd transcriptions/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Using the API

If you've exposed the backend service (either via Docker port mapping or running locally), you can interact with the API directly. The base URL will be `http://<your-host-ip>:6005/api`.

#### Endpoints

1.  **Upload & Transcribe Audio**
    *   **URL:** `/upload`
    *   **Method:** `POST`
    *   **Content-Type:** `multipart/form-data`
    *   **Form Data:**
        *   `file`: The audio file to transcribe (required).
        *   `currentModelProvider`: The provider to use: `groq`, `gemini`, `fireworks`, or `elevenlabs` (required).
        *   **Provider Specific Fields (required based on `currentModelProvider`):**
            *   If `groq`: `groqModelValue`, `groqPromptValue` (optional), `groqLanguageValue`.
            *   If `gemini`: `geminiModelValue`, `geminiPromptValue` (optional, defaults to value in `.env`).
            *   If `fireworks`: `fireworksModelValue`, `fireworksLanguageValue`.
            *   If `elevenlabs`: `elevenlabsModelValue`.
        *   `webhookUrl`: A URL to send the transcription result to via a POST request (optional).
    *   **Success Response (200 OK):**
        ```json
        {
          "transcription": "The transcribed text..."
        }
        ```
    *   **Error Responses:**
        *   `400 Bad Request`: Missing file, invalid provider, or unsupported file type.
        *   `429 Too Many Requests`: Rate limit exceeded.
        *   `500 Internal Server Error`: Backend processing error.
    *   **Example (using curl):**
        ```bash
        curl -X POST -F "file=@/path/to/your/audio.mp3" \
             -F "currentModelProvider=groq" \
             -F "groqModelValue=whisper-large-v3" \
             -F "groqLanguageValue=en" \
             http://<your-host-ip>:6005/api/upload
        ```

2.  **Get Transcription History**
    *   **URL:** `/history`
    *   **Method:** `GET`
    *   **Success Response (200 OK):** An array of history items.
        ```json
        [
          {
            "date": "26-07-2024",
            "fileExtension": "mp3",
            "fileNameNoExt": "myaudio",
            "filename": "myaudio.mp3",
            "transcription": "The transcribed text..."
          },
          // ... more items
        ]
        ```
    *   **Error Responses:**
        *   `500 Internal Server Error`: Error reading history.
    *   **Example (using curl):**
        ```bash
        curl http://<your-host-ip>:6005/api/history
        ```

3.  **Delete History Item**
    *   **URL:** `/delete`
    *   **Method:** `POST`
    *   **Content-Type:** `application/json`
    *   **Request Body:**
        ```json
        {
          "filename": "myaudio.mp3"
        }
        ```
        *(Note: Use the original filename as returned by the `/history` endpoint)*
    *   **Success Response (200 OK):**
        ```json
        {
          "success": true,
          "message": "Deleted myaudio.mp3"
        }
        ```
    *   **Error Responses:**
        *   `400 Bad Request`: Missing filename in request body.
        *   `404 Not Found`: The specified file doesn't exist in the history.
        *   `500 Internal Server Error`: Error during deletion.
    *   **Example (using curl):**
        ```bash
        curl -X POST -H "Content-Type: application/json" \
             -d '{"filename": "myaudio.mp3"}' \
             http://<your-host-ip>:6005/api/delete
        ```

#### Rate Limiting

The API endpoints have rate limits configured in the `.env` file (`TRANSCRIPTION_RATE_LIMIT`, `HISTORY_RATE_LIMIT`, `DELETE_RATE_LIMIT`). These limits are applied per IP address. If you exceed the limit, you will receive a `429 Too Many Requests` response.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
