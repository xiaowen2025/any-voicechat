# API Documentation

## Backend Stack

The backend of this application is built with a modern Python stack, prioritizing performance, developer efficiency, and scalability. The key technologies used are:

- **FastAPI**: A high-performance web framework for building APIs with Python. It's chosen for its speed, automatic interactive documentation (via Swagger UI and ReDoc), and its use of standard Python type hints for data validation.

- **`google-genai`**: The Python SDK for Google's generative AI models. Used for avatar generation and conversation analysis.  

- **`google-adk`**: Google Agent Development Kit (ADK) for building streaming agent service.

- **WebSockets**: The `websockets` library is used for real-time, bidirectional communication between the client and the server. This is essential for features that require instant updates, such as live chat or notifications.

- **Pydantic**: A library for data validation and settings management using Python type annotations. FastAPI is built on top of Pydantic, and it's used throughout the application to ensure that data conforms to the expected schema.

- **Pytest**: A popular testing framework for Python. It's used to write and run the automated tests for the backend, ensuring code quality and reliability.

## Folder Structure

```
api/
├── __init__.py
├── create_agent.py
├── exceptions.py
├── main.py
├── routers/
│   ├── analyse.py
│   ├── api_key.py
│   ├── apps.py
│   └── avatar.py
├── services/
│   ├── __init__.py
│   ├── agent_service.py
│   ├── analysis_service.py
│   └── app_service.py
├── settings.py
└── websocket/
    ├── __init__.py
    ├── connection.py
    ├── messaging.py
    └── session.py
```

## File Descriptions

### `api/main.py`
This is the main entry point of the FastAPI application. It initializes the FastAPI app, includes all the API routers from other files, mounts the static frontend files, and sets up centralized exception handling.

### `api/create_agent.py`
This file is responsible for creating a Gemini AI agent instance. It formats the agent's instructions and context before creating the agent using the `agent_service`.

### `api/exceptions.py`
This file defines custom exception classes for the application, such as `ApiKeyError`, `ImageGenerationError`, `AppNotFoundError`, and `MalformedAppConfigError`. This allows for more specific error handling in `main.py`.

### `api/settings.py`
This file defines Pydantic models for application settings, used for type hinting and validation. It includes `AppSettings` for agent configuration.

### `api/routers/`
This directory contains the API routers for different endpoints.

#### `api/routers/analyse.py`
This file defines the `/api/analyse` endpoint, which uses the `analysis_service` to analyze notes with the Gemini AI model.

#### `api/routers/api_key.py`
This file provides endpoints for verifying and setting the Gemini API key. It includes `/api/verify_api_key` and `/api/set_api_key`.

#### `api/routers/apps.py`
This file handles retrieving app configurations. It has endpoints to get a list of all available apps (`/api/apps`) and to get the settings for a specific app (`/api/apps/{app_id}/settings`), using the `app_service`.

#### `api/routers/avatar.py`
This file contains the logic for generating an avatar image. The `/api/avatar/generate` endpoint uses a generative AI model to create an image based on the agent's description and context.

### `api/services/`
This directory contains services that encapsulate business logic.

#### `api/services/agent_service.py`
This service contains a function to create a Google AI agent instance with a specified model and instructions.

#### `api/services/analysis_service.py`
This service contains the logic for analyzing notes with the Gemini AI model.

#### `api/services/app_service.py`
This service handles the logic for managing and retrieving application configurations from JSON files.

### `api/websocket/`
This directory contains the logic for handling websocket connections.

#### `api/websocket/connection.py`
This file manages the websocket lifecycle. It defines the main websocket endpoint (`/ws/{user_id}`), handles client connections and disconnections, and orchestrates the communication between the client and the agent.

#### `api/websocket/messaging.py`
This file contains the logic for exchanging messages between the client and the agent over the websocket. It handles both incoming and outgoing messages, including text and audio data.

#### `api/websocket/session.py`
This file handles the agent session for a websocket connection. It creates a runner, a session, and a request queue for the agent.

## Refactoring Suggestions

Based on a review of the codebase, here are some suggestions for refactoring and improvement:

### 1. Centralized Configuration and Secrets Management
- **API Key Handling**: The current implementation in `api/routers/api_key.py` and `api/create_agent.py` sets the Gemini API key as an environment variable. This is not a secure practice for production environments.
  - **Suggestion**: Use a dedicated secrets management tool (e.g., HashiCorp Vault, AWS Secrets Manager) to store sensitive information like API keys. For local development, `python-dotenv` is a good option, but the key should not be hardcoded or passed around in environment variables in production.
- **Hardcoded Values**: Model names and other settings are hardcoded in `api/settings.py`.
  - **Suggestion**: Move these settings to a configuration file (e.g., `config.yaml`, `.env`) and use a library like `pydantic-settings` to load them. This makes the application more configurable without changing the code.

### 2. Improved Error Handling in Websockets
- **Generic Exception Handling**: The websocket error handling in `api/websocket/connection.py` is very generic.
  - **Suggestion**: Implement more specific error handling for different types of websocket errors (e.g., `SessionCreationError`, `MessageHandlingError`). This will make the websocket communication more robust and easier to debug.

### 3. Code Structure and Reusability
- **Code Duplication**: The logic for preparing the `context` dictionary is duplicated in `api/create_agent.py` and `api/services/analysis_service.py`.
  - **Suggestion**: Create a helper function (e.g., in a `utils.py` file) to extract and format the context from the settings. This will reduce code duplication and improve maintainability.
- **Refactor Large Functions**: Functions like `generate_image` in `api/routers/avatar.py` and the messaging functions in `api/websocket/messaging.py` are doing too much.
  - **Suggestion**: Break down these large functions into smaller, single-responsibility functions. For example, in `generate_image`, you could have separate functions for creating the client, preparing the request, and processing the response.
