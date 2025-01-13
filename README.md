# Voice Assistant
A voice-activated assistant built with Python, leveraging SpeechRecognition for voice commands, ElevenLabs for natural text-to-speech, and OpenAI GTP-4 for intelligent conversation. Additionally, this assistant can integrate with your Outlook calendar via the Outlook COM Automation interface.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Future Plans](#future-plans)

## Overview
This project is a voice assistant that listens for a wake phrase ("hey assistant") and then accepts voice commands. Depending on the user's command, the assistant can:
- Respond with **OpenAI GPT-4** for general questions.
- Use **ElevenLabs** for more natural TTS output.
- Manage and update your **Outlook** calendar.

## Features
1. **Wake Phrase Detection**: Constantly listens for "hey assistant" without blocking other tasks.
2. **Speech Recognition**: Uses Google's `speech_recognition` to parse spoken commands.
3. **GPT Integration**: Offloads open-ended queries to GPT-4 via the OpenAI API.
4. **Natural TTS**: Uses ElevenLab's streaming feature for near-instant, high-quality spoken output.
5. **Outlook Calendar Automation**: Adds, modifies, or deletes events from your local Outlook installation on Windows.

## Requirements
- Python 3.7+ (recommended 3.9 or above)
- Pip / venv (or an equivalent environment manager)
- Microphone (for speech input)
- Speakers or audio output device
- Internet connection (for GPT and ElevenLabs calls)

## Python Libraries
1. `speechrecognition`
2. `pyttsx3` (in the event that ElevenLabs gets removed)
3. `elevenlabs`
4. `openai`
5. `python-dotenv`
6. `pywin32` (for Outlook integration on Windows)

## External Dependencies
- **FFmpeg** (for audio handling, needed by ElevenLabs streaming)
- **mpv** (for real-time streamed audio playback, if you're using `stream()`)

## Installation 
1. Clone the Repository (or download the zip):
    `git clone https://github.com/Balthizar01/voice-assistant.git`

2. Create and Activate a Virtual Environment
    `python -m venv venv`
    `source venv/bin/activate`

3. Install Dependencies:
    `pip install speechrecognition pyttsx3 openai python-dotenv pywin32 elevenlabs`

4. Install FFmpeg and mpv:
    - On Windows, download from ffmpeg.org and mpv.io; add them to your PATH environment variable
    - On macOS, use Homebrew: `brew install ffmpeg mpv`
    - On Linux, use your distro's package manager (e.g., `sudo apt install ffpmeg mpv`).

## Configuration
1. Create a `.env` file in the project root (this file is in `.gitignore` so it won't commit):
    `touch .env`

2. Add your API keys to `.env`:
`OPENAI_API_KEY=sk-your-openai-key`
`ELEVENLABS_API_KEY=your-elevenlabs-key`

3. Optional: Add any other env variables you want to keep secret.

## Usage
1. Run the assistant
    `python main.py`

2. Speak "Hey Assistant" once it starts. Wait for the prompt that it's ready to listen for a command/

3. Give a command, for example:
    - "Add a meeting on Thursday at 2PM"
    - "What's the capital of France?"
    - "Update my calendar event for tomorrow"

4. The assistant should:
    - Detect your command,
    - Possibly ask for missing details,
    - Call the Outlook COM interface or send a query to GPT-4,
    - Then respond with a voice powered by ElevenLabs TTS.

## Future Plans
- More natural date/time parsing with `dateparser` or `duckling`
- Additional commands (e.g., controlling system tasks, playing music, or reading emails).
- Better error handling and dialogues (e.g., "I couldn't parse that date; please repeat").