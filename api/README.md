# API Documentation

This document provides an overview of the `api/` directory, its structure, and the purpose of each file. It also includes refactoring suggestions for improving the codebase.

## Folder Structure

```
api/
├── __init__.py
├── analyse.py
├── api_key.py
├── apps.py
├── avatar.py
├── default_settings.json
├── main.py
├── services/
│   ├── __init__.py
│   └── google_ai.py
├── settings.py
├── voice_agent.py
└── websocket/
    ├── agent.py
    ├── connection.py
    └── messaging.py
```

## File Descriptions

### `api/main.py`
# This is the main entry point of the FastAPI application. It initializes the FastAPI app, includes all the API routers from other files, and mounts the static frontend files.

### `api/analyse.py`
# This file defines the `/api/analyse` endpoint, which uses the Gemini AI model to analyze notes provided in the request.

### `api/api_key.py`
# This file provides endpoints for verifying and setting the Gemini API key. It includes `/api/verify_api_key` and `/api/set_api_key`.

### `api/apps.py`
# This file handles retrieving app configurations. It has endpoints to get a list of all available apps (`/api/apps`) and to get the settings for a specific app (`/api/apps/{app_id}/settings`).

### `api/avatar.py`
# This file contains the logic for generating an avatar image. The `/api/avatar/generate` endpoint uses a generative AI model to create an image based on the agent's description and context.

### `api/default_settings.json`
# A JSON file containing the default settings for the application.

### `api/settings.py`
# This file defines the `Settings` Pydantic model, which is used for type hinting and validation of application settings. It also contains constants for file paths and model names.

### `api/voice_agent.py`
# This file is responsible for creating a "live agent" instance. It formats the agent's instructions and context before creating the agent using the `google_ai` service.

### `api/services/__init__.py`
# An empty file that marks the `services` directory as a Python package.

### `api/services/google_ai.py`
# This service file contains a function to create a Google AI agent instance with a specified model and instructions.

### `api/websocket/agent.py`
# This file handles the agent session for a websocket connection. It creates a runner, a session, and a request queue for the agent.

### `api/websocket/connection.py`
# This file manages the websocket lifecycle. It defines the main websocket endpoint (`/ws/{user_id}`), handles client connections and disconnections, and orchestrates the communication between the client and the agent.

### `api/websocket/messaging.py`
# This file contains the logic for exchanging messages between the client and the agent over the websocket. It handles both incoming and outgoing messages, including text and audio data.

## Refactoring Suggestions

Based on a review of the codebase, here are some suggestions for refactoring and improvement:

### 1. Centralized Configuration and Secrets Management
- **API Key Handling**: The current implementation in `api/api_key.py` sets the Gemini API key as an environment variable. This is not a secure practice for production environments.
  - **Suggestion**: Use a dedicated secrets management tool (e.g., HashiCorp Vault, AWS Secrets Manager) to store sensitive information like API keys. For local development, `python-dotenv` is a good option, but the key should not be hardcoded or passed around in environment variables in production.
- **Hardcoded Values**: Model names and other settings are hardcoded in `api/settings.py`.
  - **Suggestion**: Move these settings to a configuration file (e.g., `config.yaml`, `.env`) and use a library like `pydantic-settings` to load them. This makes the application more configurable without changing the code.

### 2. Improved Error Handling
- **Specific Exceptions**: The error handling in `api/avatar.py` and `api/apps.py` is very generic.
  - **Suggestion**: Create custom exception classes for different types of errors (e.g., `ApiKeyError`, `ImageGenerationError`). This will make the error handling more specific and easier to debug. Log the full error for internal review while returning a user-friendly message to the client.

### 3. Code Structure and Reusability
- **Code Duplication**: The logic for preparing the `context` dictionary is duplicated in `api/analyse.py` and `api/voice_agent.py`.
  - **Suggestion**: Create a helper function (e.g., in a `utils.py` file) to extract and format the context from the settings. This will reduce code duplication and improve maintainability.
- **Missing `__init__.py`**: The `api/websocket` directory is missing an `__init__.py` file.
  - **Suggestion**: Add an empty `__init__.py` file to the `api/websocket` directory to ensure it is treated as a Python package.
- **Refactor Large Functions**: Functions like `generate_image` in `api/avatar.py` and the messaging functions in `api/websocket/messaging.py` are doing too much.
  - **Suggestion**: Break down these large functions into smaller, single-responsibility functions. For example, in `generate_image`, you could have separate functions for creating the client, preparing the request, and processing the response.
