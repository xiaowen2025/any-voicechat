import { ref } from 'vue';

const defaultSettings = {
    "app_name": "Language Pal",
    "agent_description": "A friendly and patient native speaker to help you practice a new language.",
    "context_dict": {
        "target_language": {
            "description": "The language the user wants to practice speaking.",
            "value": "German"
        },
        "user_proficiency": {
            "description": "The user's self-assessed proficiency level in the target language.",
            "value": "Beginner (A2)"
        },
        "conversation_style": {
            "description": "The manner in which the conversation is conducted.",
            "value": "Casual and friendly"
        }
    },
    "goal_description": "To improve the user's conversational fluency and confidence in the target language by engaging in realistic dialogue.",
    "notes_taking_instruction": "After the user speaks anything, write down exactly what they spoke in the original language.",
    "analyse_instruction": "Review the user's responses and provide better alternatives or corrections to help them improve their language skills. Keep it concise and focused on practical improvements."
};

export function useSettings() {
  const settings = ref({});

  function loadSettings() {
    const storedSettings = localStorage.getItem('settings');
    if (storedSettings) {
      settings.value = JSON.parse(storedSettings);
    } else {
      settings.value = defaultSettings;
      localStorage.setItem('settings', JSON.stringify(defaultSettings));
    }
    return settings.value;
  }

  function saveSettings(newSettings) {
    localStorage.setItem('settings', JSON.stringify(newSettings));
    settings.value = newSettings;
  }

  function getContext() {
    return settings.value.context_dict || {};
  }

  function updateContext(contextName, content) {
    if (settings.value.context_dict && settings.value.context_dict[contextName]) {
      settings.value.context_dict[contextName].value = content;
      saveSettings(settings.value);
    }
  }

  return {
    settings,
    loadSettings,
    saveSettings,
    getContext,
    updateContext,
  };
}
