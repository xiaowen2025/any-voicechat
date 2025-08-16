import json
import os

# Get the absolute path to the project's root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def export_openapi_schema():
    """
    Exports the FastAPI OpenAPI schema to a JSON file.
    """
    # Late import to avoid circular dependencies and to ensure the app is fully initialized
    from api.main import app  

    # Generate the OpenAPI schema
    openapi_schema = app.openapi()

    # Add WebSocket documentation
    openapi_schema["paths"]["/ws/{user_id}"] = {
        "post": {
            "summary": "WebSocket connection",
            "description": (
                "Establishes a WebSocket connection for real-time communication with an agent."
                "The `is_audio` query parameter should be set to `true` for audio-based interactions."
                "\n\n**Protocol:**\n1. Client connects to the WebSocket endpoint."
                "\n2. Client sends a `SettingsMessage` to configure the agent."
                "\n3. Client and agent exchange messages (`TextMessage`, `AudioMessage` from client;"
                " `AgentTextMessage`, `AgentAudioMessage`, etc. from agent)."
            ),
            "parameters": [
                {
                    "name": "user_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                    "description": "The ID of the user establishing the connection.",
                },
                {
                    "name": "is_audio",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "boolean"},
                    "description": "Specifies if the session will handle audio.",
                },
            ],
            "requestBody": {
                "description": "Initial settings message to configure the agent.",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "example": "settings"},
                                "settings": {"$ref": "#/components/schemas/AppSettings"},
                            },
                        }
                    }
                },
            },
            "responses": {
                "101": {
                    "description": "Switching Protocols. The connection is upgraded to a WebSocket.",
                }
            },
        }
    }

    # Define the output path for the openapi.json file
    output_path = os.path.join(ROOT_DIR, "docs", "api-docs", "openapi.json")

    # Write the schema to the file
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)

    print(f"✅ OpenAPI schema exported to {output_path}")

if __name__ == "__main__":
    export_openapi_schema()
