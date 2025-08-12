# Vox Hub: Echo Your Ideas.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/versions/3.12/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Vox Hub** is a versatile voice chat application.

## Features

*   **Live Transcriptoin:** Get real-time transcription of your conversation.
*   **Post-Conversation Analysis:** Receive a comprehensive analysis of the entire conversation in a clean, easy-to-read markdown format.
*   **Customizable Avatars:** Generate a unique AI avatar with a single click, tailored to your chosen scenario.
*   **Configurable Scenarios:** Easily customize the agent's role, personality, and context by editing a single JSON file. Explore different use cases in the `app_examples/` directory.

## Example Applications

![gallery](docs/imgs/apps-gallery.png)

### Language Pal
![Language Pal](docs/imgs/app-language.png)

### Comfort Chat
![Comfort Chat](docs/imgs/app-listen.png)

### Story Architect
![Story Architect](docs/imgs/app-story.png)

### Interview Simulator
![Interview Simulator](docs/imgs/app-interview.png)  


## Getting Started

Follow these steps to get Vox Hub up and running on your local machine.

### Prerequisites

*   Python 3.12 or later
*   [uv](https://github.com/astral-sh/uv) (a fast Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/vox-hub.git
    cd vox-hub
    ```

2.  **Make the run script executable:**

    ```bash
    chmod +x run.sh
    ```

3.  **Build and launch the application:**

    ```bash
    ./run.sh
    ```

    This script will:
    *   Create a virtual environment.
    *   Install the required Python and Node.js dependencies.
    *   Start the backend and frontend servers.

4.  **Access the application:**

    Open your web browser and navigate to `http://localhost:8000`.

## Configuration

To customize the AI agent, you can modify the JSON configuration files located in the `app_examples/` directory. These files allow you to define the agent's personality, role, and the context of the conversation.

For example, to start a new chat with the "Story Architect" persona, you can use the `story_architect.json` file.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.