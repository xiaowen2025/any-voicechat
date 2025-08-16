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
