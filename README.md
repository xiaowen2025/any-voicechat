# AnyVoiceChat
A general-purpose voice chat agent framework with real-time note-taking and post-conversation analysis, powered by Gemini Live API. It can be easily configured for various scenarios, from interview simulations to creative brainstorming partners.  

See example app configurations under `app_examples/`.

## Example Apps  
### Interview Simulator
![2](docs/imgs/app-interview.png)
---
### Language Pal
![1](docs/imgs/app-language.png)  
---
### Friendly Listener
![3](docs/imgs/app-listen.png)   
---  
### Story Architect
![4](docs/imgs/app-story.png)

## Get Started
Make the script executable, build and launch the application.
```bash
chmod +x run.sh
./run.sh
```

You can then access the application in your web browser at `http://localhost:8000`.

## Key Features

- **Real-time Voice Interaction:** Engage in natural, real-time conversations with an AI agent.
    
- **Live Note-Taking:** Receive detailed notes on your side of the conversation in real-time.
    
- **Configurable Agent Personality:** Easily customize the agent's role, personality, and context by modifying a JSON configuration file. See `app_examples/` for different use-cases like `story_architect.json`.

- **Post-Conversation Analysis:** Get a comprehensive analysis of the conversation, presented in a clear markdown format.
    