# OpenAI Agent SDK Integration for Vocalis

This document describes the OpenAI Agent SDK integration for the Vocalis speech-to-speech AI assistant.

## Overview

The Vocalis backend now supports both local AI services and OpenAI Agent SDK, allowing users to choose between:
- **Local AI**: Uses local LLM (via LM Studio) and local TTS (via Orpheus-FASTAPI)
- **OpenAI Agent SDK**: Uses OpenAI's GPT models and TTS API for enhanced capabilities

## Configuration

### Environment Variables

Add the following to your `backend/.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
OPENAI_TTS_VOICE=alloy
OPENAI_TTS_MODEL=tts-1
USE_OPENAI=false
```

### Configuration Options

- **OPENAI_API_KEY**: Your OpenAI API key (required for OpenAI integration)
- **OPENAI_MODEL**: OpenAI model to use (default: `gpt-4o`)
- **OPENAI_TTS_VOICE**: TTS voice (options: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`)
- **OPENAI_TTS_MODEL**: TTS model (options: `tts-1`, `tts-1-hd`)
- **USE_OPENAI**: Set to `true` to enable OpenAI Agent SDK (default: `false`)

## Architecture

### Service Integration

The integration maintains backward compatibility while adding OpenAI support:

1. **Configuration System**: Enhanced to support both local and OpenAI services
2. **Service Initialization**: Automatically initializes OpenAI Agent when configured
3. **WebSocket Handler**: Routes requests to appropriate service based on configuration
4. **Fallback Support**: Falls back to local AI if OpenAI is not configured or fails

### Key Components

#### 1. OpenAIAgent Service (`backend/services/openai_agent.py`)
- Handles OpenAI API communication
- Manages conversation history
- Provides text-to-speech via OpenAI TTS
- Maintains conversation context

#### 2. Enhanced Configuration (`backend/config.py`)
- Added OpenAI-specific configuration options
- Supports environment variable overrides
- Provides unified configuration access

#### 3. Updated WebSocket Handler (`backend/routes/websocket.py`)
- Detects OpenAI Agent availability
- Routes requests to appropriate service
- Maintains consistent message format
- Handles both local and OpenAI TTS

## Usage

### Enabling OpenAI Integration

1. **Set your OpenAI API key** in `backend/.env`:
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

2. **Enable OpenAI integration**:
   ```env
   USE_OPENAI=true
   ```

3. **Optional**: Configure model and voice preferences:
   ```env
   OPENAI_MODEL=gpt-4-turbo
   OPENAI_TTS_VOICE=nova
   OPENAI_TTS_MODEL=tts-1-hd
   ```

### Running the Application

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the backend**:
   ```bash
   python -m backend.main
   ```

3. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

### Testing the Integration

Run the test script to verify OpenAI integration:

```bash
python test_openai_integration.py
```

## Features

### 1. Automatic Service Selection
- System automatically uses OpenAI Agent when `USE_OPENAI=true` and API key is configured
- Falls back to local AI services if OpenAI is not available
- No changes required to frontend code

### 2. Conversation History
- Maintains conversation context across both local and OpenAI modes
- Supports session management and conversation storage
- Preserves user profile and system prompts

### 3. Vision Integration
- Works with existing vision capabilities
- Processes images with SmolVLM and uses context with OpenAI
- Maintains vision context in conversation history

### 4. TTS Integration
- Uses OpenAI's high-quality TTS when OpenAI Agent is active
- Falls back to local TTS when using local AI
- Maintains consistent audio streaming format

## Benefits

### OpenAI Agent SDK Advantages
- **Higher Quality**: Access to state-of-the-art GPT models
- **Better TTS**: High-quality text-to-speech with multiple voice options
- **Reliability**: Stable API with consistent performance
- **Advanced Features**: Access to latest OpenAI capabilities

### Local AI Advantages
- **Privacy**: All processing happens locally
- **Cost**: No API usage costs
- **Customization**: Full control over models and parameters
- **Offline**: Works without internet connection

## Migration Guide

### From Local AI to OpenAI

1. **Backup your configuration**:
   ```bash
   cp backend/.env backend/.env.backup
   ```

2. **Add OpenAI configuration** to `backend/.env`:
   ```env
   OPENAI_API_KEY=your_api_key
   USE_OPENAI=true
   ```

3. **Test the integration**:
   ```bash
   python test_openai_integration.py
   ```

4. **Start the application** - it will automatically use OpenAI

### From OpenAI to Local AI

1. **Disable OpenAI** in `backend/.env`:
   ```env
   USE_OPENAI=false
   ```

2. **Ensure local services** are running:
   - LM Studio on `http://127.0.0.1:1234`
   - Orpheus-FASTAPI on `http://localhost:5005`

3. **Start the application** - it will automatically use local AI

## Troubleshooting

### Common Issues

1. **OpenAI API Key Not Working**
   - Verify your API key is valid and has sufficient credits
   - Check for typos in the `.env` file
   - Ensure `USE_OPENAI=true` is set

2. **OpenAI Service Not Initializing**
   - Check internet connection
   - Verify API key permissions
   - Check for rate limits or quota issues

3. **TTS Not Working with OpenAI**
   - Verify TTS model and voice are valid
   - Check audio format compatibility
   - Ensure sufficient API credits

4. **Fallback to Local AI Not Working**
   - Verify local services are running
   - Check local API endpoints in configuration
   - Ensure `USE_OPENAI=false` when testing local mode

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export LOG_LEVEL=DEBUG
```

## Performance Considerations

### OpenAI Mode
- **Latency**: Dependent on OpenAI API response times
- **Cost**: Based on API usage (tokens and TTS characters)
- **Rate Limits**: Subject to OpenAI API rate limits

### Local AI Mode
- **Latency**: Dependent on local hardware and model size
- **Cost**: No API costs, but requires local compute resources
- **Rate Limits**: No external rate limits

## Future Enhancements

1. **Hybrid Mode**: Use OpenAI for complex queries, local AI for simple ones
2. **Model Selection**: Allow per-request model selection
3. **Cost Monitoring**: Track and display API usage costs
4. **Batch Processing**: Optimize for multiple simultaneous requests

## Support

For issues with the OpenAI integration:
1. Check the troubleshooting section above
2. Verify your OpenAI API key and account status
3. Test with the provided test script
4. Check application logs for detailed error messages

For local AI issues:
1. Ensure local services are running and accessible
2. Verify API endpoints in configuration
3. Check service-specific logs for errors
