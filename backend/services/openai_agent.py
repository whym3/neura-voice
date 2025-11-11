"""
OpenAI Agent Service

Handles communication with OpenAI's Agent SDK for speech-to-speech capabilities.
"""

import os
import json
import logging
import base64
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from openai import OpenAI
from openai.types.chat import ChatCompletion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIAgent:
    """
    Client for communicating with OpenAI's Agent SDK.
    
    This class handles speech-to-speech interactions using OpenAI's
    native audio capabilities and agent functionality.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        timeout: int = 60
    ):
        """
        Initialize the OpenAI Agent client.
        
        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # State tracking
        self.is_processing = False
        self.conversation_history = []
        
        logger.info(f"Initialized OpenAI Agent with model={model}")
    
    def add_to_history(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: Message role ('system', 'user', or 'assistant')
            content: Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Allow deeper history for models with large context windows
        if len(self.conversation_history) > 50:
            # Always keep the system message if it exists
            if self.conversation_history[0]["role"] == "system":
                self.conversation_history = (
                    [self.conversation_history[0]] + 
                    self.conversation_history[-49:]
                )
            else:
                self.conversation_history = self.conversation_history[-50:]
    
    def get_response(self, user_input: str, system_prompt: Optional[str] = None, 
                    add_to_history: bool = True, temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Get a response from the OpenAI model for the given user input.
        
        Args:
            user_input: User's text input
            system_prompt: Optional system prompt to set context
            add_to_history: Whether to add this exchange to conversation history
            temperature: Optional temperature override (0.0 to 1.0)
            
        Returns:
            Dictionary containing the OpenAI response and metadata
        """
        self.is_processing = True
        
        try:
            # Prepare messages
            messages = []
            
            # Add system prompt if provided and not already in history
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user input to history if it's not empty and add_to_history is True
            if user_input.strip() and add_to_history:
                self.add_to_history("user", user_input)
            
            # Add conversation history (which now includes the user input if add_to_history=True)
            messages.extend(self.conversation_history)
            
            # Only add user input directly if not adding to history
            if user_input.strip() and not add_to_history:
                messages.append({
                    "role": "user",
                    "content": user_input
                })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract assistant response
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history (only if we added the user input)
            if assistant_message and add_to_history:
                self.add_to_history("assistant", assistant_message)
            
            logger.info(f"Received response from OpenAI API")
            
            return {
                "text": assistant_message,
                "processing_time": None,  # OpenAI doesn't provide this directly
                "finish_reason": response.choices[0].finish_reason,
                "model": response.model
            }
            
        except Exception as e:
            logger.error(f"OpenAI API request error: {e}")
            error_response = f"I'm sorry, I encountered a problem connecting to OpenAI. {str(e)}"
            
            # Add the error to history if requested
            if add_to_history:
                self.add_to_history("assistant", error_response)
            
            return {
                "text": error_response,
                "error": str(e)
            }
        finally:
            self.is_processing = False
    
    async def text_to_speech(self, text: str, voice: str = "alloy", model: str = "tts-1") -> bytes:
        """
        Convert text to speech using OpenAI's TTS API.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: TTS model to use (tts-1, tts-1-hd)
            
        Returns:
            bytes: Audio data in MP3 format
        """
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            
            # Get the audio data as bytes
            audio_data = response.content
            
            logger.info(f"Generated TTS audio for {len(text)} characters")
            return audio_data
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            raise e
    
    async def speech_to_text(self, audio_data: bytes, model: str = "whisper-1") -> str:
        """
        Convert speech to text using OpenAI's Whisper API.
        
        Args:
            audio_data: Audio data bytes
            model: Whisper model to use
            
        Returns:
            str: Transcribed text
        """
        try:
            # Save audio data to a temporary file for OpenAI API
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file.flush()
                
                # Transcribe using OpenAI Whisper
                with open(temp_file.name, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model=model,
                        file=audio_file,
                        response_format="text"
                    )
                
                # Clean up temp file
                os.unlink(temp_file.name)
            
            logger.info(f"Transcribed audio to text: {len(transcript)} characters")
            return transcript
            
        except Exception as e:
            logger.error(f"OpenAI speech-to-text error: {e}")
            raise e
    
    def clear_history(self, keep_system_prompt: bool = True) -> None:
        """
        Clear conversation history.
        
        Args:
            keep_system_prompt: Whether to keep the system prompt if it exists
        """
        if keep_system_prompt and self.conversation_history and self.conversation_history[0]["role"] == "system":
            self.conversation_history = [self.conversation_history[0]]
        else:
            self.conversation_history = []
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the current configuration.
        
        Returns:
            Dict containing the current configuration
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
            "is_processing": self.is_processing,
            "history_length": len(self.conversation_history)
        }
