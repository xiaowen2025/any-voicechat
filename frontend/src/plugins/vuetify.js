// frontend/src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import { themes as customThemes } from '@/themes';
import { nextTick } from 'vue';

function generateVuetifyThemes(themes) {
  const vuetifyThemes = {};
  if (!themes) {
    return vuetifyThemes;
  }
  for (const themeName in themes) {
    if (Object.prototype.hasOwnProperty.call(themes, themeName)) {
      const theme = themes[themeName];
      if (theme && theme.light && theme.dark) {
        vuetifyThemes[themeName] = {
          dark: false,
          colors: theme.light,
        };
        vuetifyThemes[`${themeName}Dark`] = {
          dark: true,
          colors: theme.dark,
        };
      }
    }
  }
  return vuetifyThemes;
}

export const themes = generateVuetifyThemes(customThemes);

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    themes,
  },
  defaults: {
    VBtn: {
      borderRadius: '8px',
    },
    VCard: {
      borderRadius: '8px',
    },
    VTextField: {
      borderRadius: '8px',
    },
    VTextarea: {
      borderRadius: '8px',
    },
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: {
      fontSize: '6rem',
      fontWeight: 300,
      lineHeight: '6rem',
      letterSpacing: '-0.09375em',
    },
    h2: {
      fontSize: '3.75rem',
      fontWeight: 300,
      lineHeight: '3.75rem',
      letterSpacing: '-0.03125em',
    },
    h3: {
      fontSize: '3rem',
      fontWeight: 400,
      lineHeight: '3.125rem',
      letterSpacing: 'normal',
    },
    h4: {
      fontSize: '2.125rem',
      fontWeight: 400,
      lineHeight: '2.5rem',
      letterSpacing: '0.015625em',
    },
    h5: {
      fontSize: '1.5rem',
      fontWeight: 400,
      lineHeight: '2rem',
      letterSpacing: 'normal',
    },
    h6: {
      fontSize: '1.25rem',
      fontWeight: 500,
      lineHeight: '2rem',
      letterSpacing: '0.009375em',
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: '1.75rem',
      letterSpacing: '0.009375em',
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: '1.375rem',
      letterSpacing: '0.00625em',
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: '1.5rem',
      letterSpacing: '0.03125em',
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: '1.25rem',
      letterSpacing: '0.015625em',
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: '2.25rem',
      letterSpacing: '0.078125em',
      textTransform: 'uppercase',
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: '1.25rem',
      letterSpacing: '0.025em',
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 500,
      lineHeight: '2rem',
      letterSpacing: '0.09375em',
      textTransform: 'uppercase',
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept('@/themes', async (newThemes) => {
    const newVuetifyThemes = generateVuetifyThemes(newThemes.themes);
    vuetify.theme.themes.value = { ...vuetify.theme.themes.value, ...newVuetifyThemes };

    const currentThemeName = vuetify.theme.global.name.value;
    vuetify.theme.global.name.value = 'temp-theme-for-reload';
    await nextTick();
    vuetify.theme.global.name.value = currentThemeName;
  });
}

export default vuetify;