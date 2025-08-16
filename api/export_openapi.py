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

    # Define the output path for the openapi.json file
    output_path = os.path.join(ROOT_DIR, "docs", "api-docs", "openapi.json")

    # Write the schema to the file
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)

    print(f"✅ OpenAPI schema exported to {output_path}")

if __name__ == "__main__":
    export_openapi_schema()
