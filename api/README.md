# API Documentation

## Backend Stack

## 2. Core Stacks

The API is built on a modern Python stack, leveraging several powerful libraries and frameworks.

### FastAPI

-   **Role**: The web framework used to build the API, responsible for routing, request handling, and response generation.
-   **Why**: Asynchronous operations, easy-to-use support for WebSockets.

### `google-genai`

-   **Role**: The Python SDK for Google's generative AI models, used here for avatar generation.
-   **Why**: Balancing Cost and Performance

### `google-adk`

-   **Role**: The Google Agent Development Kit (ADK), used to build the streaming agent service.
-   **Why**: Bi-streaming support

### WebSockets

-   **Role**: Used for real-time, bidirectional communication, which is essential for the live agent feature.
-   **Why**: Web standard for real-time communication.

## Structure

The API is organized into several directories, each with a specific responsibility. This modular structure makes the codebase easier to understand, maintain, and extend.

### File Tree

```
api/
├── __init__.py                # Makes the 'api' directory a Python package.
├── API_DOCUMENTATION.md       # This documentation file.
├── README.md                  # General information about the API.
├── create_agent.py            # Script to create and configure agents.
├── exceptions.py              # Defines custom exception classes for the application.
├── main.py                    # The main entry point for the FastAPI application.
├── settings.py                # Application settings and configuration management.
├── utils.py                   # Utility functions used across the application.
│
├── routers/                   # Contains the API's route handlers.
│   ├── __init__.py
│   ├── analyse.py             # Routes for conversation analysis.
│   ├── api_key.py             # Routes for managing API keys.
│   ├── apps.py                # Routes for managing applications.
│   └── avatar.py              # Routes for generating avatars.
│
├── services/                  # Contains the business logic of the application.
│   ├── __init__.py
│   ├── agent_service.py       # Service for creating and managing AI agents.
│   ├── analysis_service.py    # Service for handling conversation analysis.
│   └── app_service.py         # Service for managing applications.
│
└── websocket/                 # Handles WebSocket connections for real-time communication.
    ├── __init__.py
    ├── connection.py          # Manages the WebSocket connection lifecycle.
    ├── messaging.py           # Handles messaging between the client and the agent.
    └── session.py             # Manages the agent session over WebSockets.
```

### Interconnections

-   **`main.py`**: This is the core of the application. It initializes the FastAPI app and includes the routers from the `routers/` directory. It also sets up exception handlers that catch custom exceptions defined in `exceptions.py`.
-   **`routers/`**: Each file in this directory defines a set of related API endpoints using FastAPI's `APIRouter`. These routers delegate the actual business logic to the services in the `services/` directory.
-   **`services/`**: This is where the main business logic resides. For example, `routers/avatar.py` calls functions in the `google-genai` library to generate an avatar, while `services/agent_service.py` creates AI agents using the `google-adk` library.
-   **`websocket/`**: This directory is dedicated to real-time communication. `websocket/connection.py` defines the WebSocket endpoint, and it uses `websocket/session.py` and `websocket/messaging.py` to manage the communication flow with the AI agent.
