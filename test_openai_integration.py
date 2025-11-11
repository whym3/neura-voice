#!/usr/bin/env python3
"""
Test script to verify OpenAI Agent SDK integration with Vocalis backend.
This script tests the basic functionality without requiring the full frontend.
"""

import sys
import os
import asyncio
import json
import base64
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.openai_agent import OpenAIAgent
from backend.config import get_config

async def test_openai_agent():
    """Test the OpenAI Agent service integration."""
    print("🧪 Testing OpenAI Agent SDK Integration...")
    
    # Load configuration
    config = get_config()
    
    # Check if OpenAI is configured
    if not config["openai_api_key"]:
        print("❌ OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env")
        print("   To test with OpenAI, set:")
        print("   - OPENAI_API_KEY=your_api_key_here")
        print("   - USE_OPENAI=true")
        return False
    
    if not config["use_openai"]:
        print("❌ OpenAI not enabled. Please set USE_OPENAI=true in backend/.env")
        return False
    
    try:
        # Initialize OpenAI Agent
        print("🔧 Initializing OpenAI Agent...")
        agent = OpenAIAgent(
            api_key=config["openai_api_key"],
            model=config["openai_model"]
        )
        
        # Test basic conversation
        print("💬 Testing conversation...")
        system_prompt = "You are a helpful assistant. Respond briefly."
        user_message = "Hello! Can you introduce yourself?"
        
        response = agent.get_response(user_message, system_prompt)
        
        print(f"✅ Conversation test successful!")
        print(f"   User: {user_message}")
        print(f"   Assistant: {response['text']}")
        
        # Test TTS
        print("🔊 Testing TTS...")
        tts_text = "Hello! This is a test of the OpenAI TTS integration."
        audio_data = await agent.text_to_speech(tts_text)
        
        print(f"✅ TTS test successful!")
        print(f"   Generated {len(audio_data)} bytes of audio data")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_configuration():
    """Test the configuration system."""
    print("⚙️ Testing configuration...")
    
    config = get_config()
    
    print(f"   USE_OPENAI: {config['use_openai']}")
    print(f"   OPENAI_MODEL: {config['openai_model']}")
    print(f"   OPENAI_TTS_VOICE: {config['openai_tts_voice']}")
    print(f"   OPENAI_TTS_MODEL: {config['openai_tts_model']}")
    
    if config["openai_api_key"]:
        print(f"   OPENAI_API_KEY: [configured]")
    else:
        print(f"   OPENAI_API_KEY: [not configured]")
    
    return True

async def main():
    """Run all tests."""
    print("🚀 Vocalis OpenAI Integration Test")
    print("=" * 50)
    
    # Test configuration
    config_ok = await test_configuration()
    if not config_ok:
        print("\n⚠️ Configuration issues detected. Please check backend/.env")
        return
    
    # Test OpenAI Agent if configured
    if get_config()["openai_api_key"] and get_config()["use_openai"]:
        agent_ok = await test_openai_agent()
        if agent_ok:
            print("\n🎉 All tests passed! OpenAI Agent SDK integration is working.")
        else:
            print("\n❌ OpenAI Agent tests failed. Please check your configuration.")
    else:
        print("\nℹ️ OpenAI not configured for testing.")
        print("   To enable OpenAI, set in backend/.env:")
        print("   - OPENAI_API_KEY=your_api_key_here")
        print("   - USE_OPENAI=true")
    
    print("\n📋 Usage Instructions:")
    print("   1. Set your OpenAI API key in backend/.env")
    print("   2. Set USE_OPENAI=true to enable OpenAI Agent")
    print("   3. Start the backend: python -m backend.main")
    print("   4. Start the frontend: cd frontend && npm run dev")
    print("   5. The system will automatically use OpenAI when configured")

if __name__ == "__main__":
    asyncio.run(main())
