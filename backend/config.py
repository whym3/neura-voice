"""
Vocalis Configuration Module

Loads and provides access to configuration settings from environment variables
and the .env file.
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# API Endpoints
LLM_API_ENDPOINT = os.getenv("LLM_API_ENDPOINT", "http://127.0.0.1:1234/v1/chat/completions")
TTS_API_ENDPOINT = os.getenv("TTS_API_ENDPOINT", "http://localhost:5005/v1/audio/speech")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "tts-1")
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"

# Whisper Model Configuration
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny.en")

# TTS Configuration
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")
TTS_VOICE = os.getenv("TTS_VOICE", "tara")
TTS_FORMAT = os.getenv("TTS_FORMAT", "wav")

# WebSocket Server Configuration
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST", "0.0.0.0")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8000))

# Audio Processing
VAD_THRESHOLD = float(os.getenv("VAD_THRESHOLD", 0.5))
VAD_BUFFER_SIZE = int(os.getenv("VAD_BUFFER_SIZE", 30))
AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", 48000))

def get_config() -> Dict[str, Any]:
    """
    Returns all configuration settings as a dictionary.
    
    Returns:
        Dict[str, Any]: Dictionary containing all configuration settings
    """
    return {
        "llm_api_endpoint": LLM_API_ENDPOINT,
        "tts_api_endpoint": TTS_API_ENDPOINT,
        "openai_api_key": OPENAI_API_KEY,
        "openai_model": OPENAI_MODEL,
        "openai_tts_voice": OPENAI_TTS_VOICE,
        "openai_tts_model": OPENAI_TTS_MODEL,
        "use_openai": USE_OPENAI,
        "whisper_model": WHISPER_MODEL,
        "tts_model": TTS_MODEL,
        "tts_voice": TTS_VOICE,
        "tts_format": TTS_FORMAT,
        "websocket_host": WEBSOCKET_HOST,
        "websocket_port": WEBSOCKET_PORT,
        "vad_threshold": VAD_THRESHOLD,
        "vad_buffer_size": VAD_BUFFER_SIZE,
        "audio_sample_rate": AUDIO_SAMPLE_RATE,
    }
